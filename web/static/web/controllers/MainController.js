angular.module("tweetscore").controller("MainController", function($scope, TwitterAPIService){
  $scope.screen_name = "";
  $scope.getTwitterData = function() {
    TwitterAPIService.getUserData(
      $scope.screen_name,
      $scope.check_count(),
      function(data){
        $scope.user = data['user']
        $scope.tweets = data['tweets']
        console.log($scope.user);
        console.log($scope.tweets);
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
  $scope.today = function() {
    return new Date();
  };
  $scope.date_end = $scope.today();

  $scope.clear = function(dt) {
    dt = null;
  };

  // $scope.inlineOptions = {
  //   customClass: getDayClass,
  //   minDate: new Date(),
  //   showWeeks: true
  // };

  $scope.dateOptions = {
    formatYear: 'yy',
    maxDate: new Date(2020, 5, 22),
    minDate: new Date(),
    startingDay: 1
  };

  // Disable weekend selection
  // function disabled(data) {
  //   var date = data.date,
  //     mode = data.mode;
  //   return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
  // }

  // $scope.toggleMin = function() {
  //   $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
  //   $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
  // };
  //
  // $scope.toggleMin();

  $scope.open1 = function() {
    $scope.popup1.opened = true;
  };

  $scope.open2 = function() {
    $scope.popup2.opened = true;
  };

  $scope.setDate = function(year, month, day) {
    $scope.dt = new Date(year, month, day);
  };

  $scope.altInputFormats = ['M!/d!/yyyy'];

  $scope.popup1 = {
    opened: false
  };

  $scope.popup2 = {
    opened: false
  };

  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var afterTomorrow = new Date();
  afterTomorrow.setDate(tomorrow.getDate() + 1);
  $scope.events = [
    {
      date: tomorrow,
      status: 'full'
    },
    {
      date: afterTomorrow,
      status: 'partially'
    }
  ];

  function getDayClass(data) {
    var date = data.date,
      mode = data.mode;
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);

      for (var i = 0; i < $scope.events.length; i++) {
        var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return $scope.events[i].status;
        }
      }
    }

    return '';
  }
  // End poop
});
