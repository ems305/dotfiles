// Github's relative dates are completely worthless. This will format all their dates properly.

var Time;
var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
Time = (function() {
  var day, days, month, months, short_days, short_months;
  days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  short_days = (function() {
    var _i, _len, _results;
    _results = [];
    for (_i = 0, _len = days.length; _i < _len; _i++) {
      day = days[_i];
      _results.push(day.slice(0, 3));
    }
    return _results;
  })();
  months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  short_months = (function() {
    var _i, _len, _results;
    _results = [];
    for (_i = 0, _len = months.length; _i < _len; _i++) {
      month = months[_i];
      _results.push(month.slice(0, 3));
    }
    return _results;
  })();
  function Time(datetext) {
    this.now = new Date;
    this.datetext = datetext || this.now;
    this.date = new Date(this.datetext);
    this.year = this.date.getFullYear();
    this.month = this.date.getMonth() + 1;
    this.day = this.date.getDate();
    this.milliseconds = this.date.getMilliseconds();
    this.day_of_week = days[this.date.getDay()];
    this.short_day_of_week = short_days[this.date.getDay()];
    this.month_of_year = months[this.date.getMonth()];
    this.short_month_of_year = short_months[this.date.getMonth()];
    this.epoch = this.date.getTime();
    this.ampm = this.date.getHours() >= 12 ? "pm" : "am";
    this.hours = __bind(function() {
      var hours;
      hours = this.date.getHours();
      if (hours === 0 || hours === 24) {
        hours = 12;
      }
      if (hours > 12) {
        hours -= 12;
      }
      if (hours < 10) {
        hours = "0" + hours;
      }
      return hours;
    }, this)();
    this.minutes = __bind(function() {
      var minutes;
      minutes = this.date.getMinutes();
      if (minutes < 10) {
        minutes = "0" + minutes;
      }
      return minutes;
    }, this)();
    this.seconds = __bind(function() {
      var seconds;
      seconds = this.date.getSeconds();
      if (seconds < 10) {
        seconds = "0" + seconds;
      }
      return seconds;
    }, this)();
    this.military_hours = this.date.getHours();
    this.military_time = "" + (this.date.getHours()) + ":" + this.minutes;
    this.time = "" + this.hours + ":" + this.minutes + this.ampm;
  }
  Time.prototype.verbose = function() {
    var date, time, today;
    today = new Time(this.now);
    date = (function() {
      switch (true) {
        case this.day === today.day:
          return "Today";
        case this.day === today.day - 1:
          return "Yesterday";
        case this.day === today.day + 1:
          return "Tomorrow";
        default:
          return "" + this.day_of_week + ", " + this.month_of_year + " " + this.day + ", " + this.year;
      }
    }).call(this);
    time = this.time;
    return "" + date + " at " + time;
  };
  Time.prototype.rails_datetime = function() {
    return "" + this.year + "-" + this.month + "-" + this.day + " " + this.military_hours + ":" + this.minutes + ":" + this.seconds;
  };
  return Time;
})();


$(function () {
  var $relativeDate = $('.js-relative-date');

  $relativeDate.each(function () {
    var time = new Time($(this).attr('title'));
    var newElement = $("<time/>").html(time.verbose());
    $(this).replaceWith(newElement);
  });
});
