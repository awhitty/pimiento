angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $firebase) {
  // Main app controller, empty for the example
  $scope.channels = $firebase(new Firebase('https://pimiento.firebaseio.com/devices/0'));

  $scope.hsv = {
    hue: 0,
    saturation: 0,
    brightness: 0
  }

  $scope.channels.$on('loaded', function() {
    $scope.$watch('channels', function(channels) {
      var red   = channels['red'].value,
          green = channels['green'].value,
          blue  = channels['blue'].value;

      hsv = rgbToHsv(red, green, blue);

      $scope.hsv = {
        hue:        hsv[0],
        saturation: hsv[1],
        brightness: hsv[2]
      }
    }, true)
  })

  $scope.$watch('hsv', function(hsv) {
    rgb = hsvToRgb(hsv.hue, hsv.saturation, hsv.brightness)

    $scope.bgstyle = rgbToHex(Math.floor(rgb[0]), Math.floor(rgb[1]), Math.floor(rgb[2]));
  }, true)

  $scope.saveChannels = function() {
    rgb = hsvToRgb($scope.hsv.hue, $scope.hsv.saturation, $scope.hsv.brightness)

    $scope.channels['red'].value   = rgb[0];
    $scope.channels['green'].value = rgb[1];
    $scope.channels['blue'].value  = rgb[2];

    $scope.channels.$save()
  }

});

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function hsvToRgb(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (h && s === undefined && v === undefined) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return [r * 255, g * 255, b * 255];
}

function rgbToHsv(r, g, b) {
  r /= 255, g /= 255, b /= 255;
 
  var max = Math.max(r, g, b), min = Math.min(r, g, b);
  var h, s, v = max;
 
  var d = max - min;
  s = max == 0 ? 0 : d / max;
 
  if (max == min) {
    h = 0; // achromatic
  } else {
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
 
    h /= 6;
  }
 
  return [ h, s, v ];
}