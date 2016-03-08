angular.module("tweetscore").controller("MainController", function($scope, TwitterAPIService){
  $scope.screen_name = "";
  $scope.getTwitterData = function() {
    TwitterAPIService.getUserData(
      $scope.screen_name,
      $scope.check_count(),
      $scope.picture_toggle,
      $scope.date_start.getTime() / 1000,
      $scope.date_end.getTime() / 1000,
      function(data){
        if (data){
          $scope.user = data['user'];
          $scope.tweets = data['tweets'];
          console.log($scope.tweets.length);
          console.log($scope.tweets);
        }
      });
  };

  // Retweet count
  $scope.all_tweets = true;
  $scope.retweet_count = "1";
  $scope.retweetPattern = /^\d+$/;
  $scope.check_count = function() {
    if ($scope.all_tweets) {
      return "all";
    } else {
      return $scope.retweet_count;
    }
  };

  // Dates
  $scope.date_start = new Date(2016, 0, 1);
  $scope.date_end = new Date();
  $scope.dateOptions = {
    formatYear: 'yy',
    maxDate: new Date(),
    minDate: new Date(1970, 1, 1),
    startingDay: 1
  };
  $scope.open1 = function() {
    $scope.popup1.opened = true;
  };
  $scope.open2 = function() {
    $scope.popup2.opened = true;
  };
  $scope.popup1 = {
    opened: false
  };
  $scope.popup2 = {
    opened: false
  };

  // Picture or no picture in tweet
  $scope.picture_toggle = "all";

  // Format twitter_score
  $scope.formatScore = function(n) {
    return Math.round(n);
  };
});
