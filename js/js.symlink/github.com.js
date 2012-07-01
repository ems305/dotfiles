// // Github's relative dates are completely worthless. This will format all their dates properly.
// 
// Date.prototype.monthOfYear = function(){
//   var months = ["January", "February", "March",
//                 "April", "May", "June", "July",
//                 "August", "September", "October",
//                 "November", "December"];
//   return months[this.getMonth()];
// }
// 
// Date.prototype.dayOfWeek = function(){
//   var days = ["Sunday", "Monday", "Tuesday", "Wednesday",
//               "Thursday", "Friday", "Saturday"];
//   return days[this.getDay()];
// }
// 
// Date.prototype.time = function(){
//   var hours = this.getHours();
//   if (hours === 0 || hours === 24) hours = 12;
//   if (hours > 12) hours -= 12;
// 
//   var minutes = this.getMinutes();
//   if (minutes < 10) minutes = "0" + minutes;
// 
//   var ampm = this.getHours() >= 12 ? "pm" : "am";
// 
//   return "" + hours + ":" + minutes + ampm;
// }
// 
// Date.prototype.verbose = function(){
//   var time = this.time();
//   var today = new Date;
//   var date = "" + this.dayOfWeek() + ", " + this.monthOfYear() + " " + this.getDate() + ", " + this.getFullYear();
// 
//   if (this.getMonth() == today.getMonth() && this.getFullYear() == today.getFullYear()) {
//     if (this.getDate() === today.getDate()) {
//       date = "Today";
//     }
//     else if (this.getDate() === today.getDate() - 1) {
//       date = "Yesterday";
//     }
//     else if (this.getDate() === today.getDate() + 1) {
//       date = "Tomorrow";
//     }
//   }
//   return "" + date + " at " + time;
// }
// 
// $(function () {
//   var $relativeDate = $('.js-relative-date');
// 
//   $relativeDate.each(function () {
//     var date = new Date($(this).attr('title'));
//     var newElement = $("<time/>").html(date.verbose());
//     $(this).replaceWith(newElement);
//   });
// });
