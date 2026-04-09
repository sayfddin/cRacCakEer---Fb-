# -*- coding: utf-8 -*-
import subprocess
import time
import sys
import threading
from queue import Queue, Empty

# --- الإعدادات ---
# اسم الملف الذي تريد تشغيله ومراقبته
SCRIPT_TO_RUN = "main.py" 
# المدة بالثواني التي اذا لم تتغير فيها الاستجابة سيتم إعادة التشغيل (دقيقتان ونصف = 150 ثانية)
RESTART_TIMEOUT_SECONDS = 150

def enqueue_output(process, queue):
    """
    هذه الدالة تعمل في خيط منفصل لقراءة مخرجات السكربت ووضعها في طابور.
    """
    try:
        # اقرأ المخرجات سطراً بسطر
        for line in iter(process.stdout.readline, ''):
            queue.put(line)
        process.stdout.close()
    except Exception:
        # قد تحدث مشكلة هنا إذا تم إيقاف العملية فجأة
        pass

def run_and_monitor():
    """
    الدالة الرئيسية التي تقوم بتشغيل ومراقبة السكربت.
    """
    # حلقة لا نهائية لضمان استمرار عمل المراقب
    while True:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] بدء تشغيل السكربت '{SCRIPT_TO_RUN}'...")
        try:
            # الأمر المستخدم لتشغيل سكربت البايثون
            process = subprocess.Popen(
                [sys.executable, SCRIPT_TO_RUN],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding='utf-8'
            )
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] تم تشغيل السكربت بنجاح. رقم العملية: {process.pid}")

        except FileNotFoundError:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] خطأ: الملف '{SCRIPT_TO_RUN}' غير موجود. يرجى التأكد من الاسم.")
            break # إنهاء المراقب إذا لم يتم العثور على الملف
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] فشل في تشغيل السكربت: {e}. المحاولة مرة أخرى بعد 10 ثواني...")
            time.sleep(10)
            continue

        # استخدم طابور (queue) للحصول على المخرجات من خيط القراءة
        output_queue = Queue()
        reader_thread = threading.Thread(target=enqueue_output, args=(process, output_queue))
        reader_thread.daemon = True  # لإنهاء الخيط عند انتهاء البرنامج الرئيسي
        reader_thread.start()

        last_output_time = time.time()

        # حلقة المراقبة للعملية الحالية
        while True:
            # 1. تحقق مما إذا توقف السكربت عن العمل
            if process.poll() is not None:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] توقف السكربت بشكل غير متوقع. سيتم إعادة التشغيل...")
                break # الخروج من حلقة المراقبة لإعادة التشغيل من الحلقة الخارجية

            # 2. تحقق من وجود استجابة جديدة
            try:
                # حاول الحصول على سطر جديد من المخرجات
                line = output_queue.get_nowait()
                # تم استلام مخرجات جديدة
                print(line, end='') # طباعة مخرجات البوت
                last_output_time = time.time() # تحديث وقت آخر استجابة
            except Empty:
                # لا توجد استجابة جديدة، تحقق من مدة التوقف
                time_since_last_output = time.time() - last_output_time
                if time_since_last_output > RESTART_TIMEOUT_SECONDS:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] لا توجد استجابة جديدة منذ أكثر من {RESTART_TIMEOUT_SECONDS} ثانية. سيتم إعادة التشغيل...")
                    process.kill() # أوقف العملية الحالية
                    process.wait() # تأكد من أنها توقفت تمامًا
                    break # الخروج من حلقة المراقبة لإعادة التشغيل

            time.sleep(1) # انتظر ثانية واحدة قبل التحقق مرة أخرى

if __name__ == "__main__":
    run_and_monitor()