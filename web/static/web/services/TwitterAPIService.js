angular.module('tweetscore').service('TwitterAPIService', function($http) {
  this.getUserData = function(screen_name, callback) {
    $http.get("/api/v1/users/"+screen_name+"/twitter_data").
    success(function(data){
      console.log(data);
      callback(data);
    }).
    error(function(error) {
      console.error(error);
      callback(null);
    });
  };
});
