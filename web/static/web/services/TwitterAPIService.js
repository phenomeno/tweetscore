angular.module('tweetscore').service('TwitterAPIService', function($http) {
  this.getUserData = function(screen_name, retweet_count, picture_toggle, date_start, date_end, callback) {
    $http.get(
      "/api/v1/users/"+screen_name+"/twitter_data",
      config= {
        params: {
          retweet_count: retweet_count,
          picture_toggle: picture_toggle,
          date_start: date_start,
          date_end: date_end
        }
      }
    ).
    success(function(data){
      callback(data);
    }).
    error(function(error) {
      callback(error);
    });
  };
});
