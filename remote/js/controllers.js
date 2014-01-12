angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $firebase) {
  // Main app controller, empty for the example
  $scope.channels = $firebase(new Firebase('https://pimiento.firebaseio.com'));
  $scope.channels.$bind($scope, "boundChannels")

  $scope.channels.$on('loaded', function() {
    $scope.$watch('channels', function(channels) {
      var red = channels[0].value * 255,
          green = channels[1].value * 255,
          blue = channels[2].value * 255;

      $scope.bgstyle = rgbToHex(Math.floor(red), Math.floor(green), Math.floor(blue));
    }, true)
  })

});

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}