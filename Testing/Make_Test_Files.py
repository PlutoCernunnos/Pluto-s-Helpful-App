import os
import time
import random

folder = os.path.join(os.path.expanduser('~'), 'Downloads')

extensions = ['.jpg', '.png', '.pdf', '.txt', '.mp3', '.wav',
              '.mp4', '.zip', '.exe', '.py', '.xyz', '.abc']

for i in range(20):
    ext = random.choice(extensions)
    filename = f"testfile_{i}{ext}"
    file_path = os.path.join(folder, filename)

    # create an empty file
    with open(file_path, 'w') as f:
        f.write("test")

    # give it a random age between 0 and 100 days
    age_days = random.randint(0, 100)
    fake_time = time.time() - (age_days * 24 * 3600)
    os.utime(file_path, (fake_time, fake_time))

    print(f"Created {filename} — {age_days} days old")