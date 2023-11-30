const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw Error('Jobs is not an array');
  }
  jobs.forEach((job) => {
    const curJob = queue.create('push_notification_code_3', job);

    curJob.save((err) => {
      if (!err) {
        console.log(`Notification job created: ${curJob.id}`);
      }
    });
    curJob.on('complete', function(result){
      console.log(`Notification job ${curJob.id} completed`);
    }).on('failed', function(errorMessage){
      console.log(`Notification job ${curJob.id} failed: ${errorMessage}`);
    }).on('progress', function(progress, data){
      console.log(`Notification job ${curJob.id} ${progress}% complete`);
    });
  });
};

module.exports = createPushNotificationsJobs;
