angular.module("tweetscore").controller("MainController", function($scope, TwitterAPIService){
  $scope.test = "hi world";
  $scope.screen_name = "";
  $scope.getUser = function() {
    TwitterAPIService.getUserData($scope.screen_name, function(data){});
  };
});
