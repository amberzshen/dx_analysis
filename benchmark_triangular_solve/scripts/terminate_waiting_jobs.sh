for job in $(cat waiting_jobs.txt); do
    dx terminate $job
done
