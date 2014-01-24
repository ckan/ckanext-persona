ckan.module('persona', function(jQuery, _) {
  return {
    initialize: function() {

      jQuery.proxyAll(this, /_on/);

      // Tell Persona what user is logged in and what functions to call when a
      // user logs in or logs out.
      // FIXME: null should be the email address of the logged-in user, when
      // someone's logged in.
      navigator.id.watch({
        loggedInUser:null,
        onlogin: this._onlogin,
        onlogout: this._onlogout
      });

      if (this.options.action == "login") {
        this.el.on('click', this._on_login_clicked);
      } else {
        this.el.on('click', this._on_logout_clicked);
      }
    },

   _on_login_clicked: function() {
     navigator.id.request();
   },

   _on_logout_clicked: function() {
     navigator.id.logout();
   },

   _onlogin: function(assertion) {
     // FIXME: Don't hardcode login URL.
     this.sandbox.jQuery.ajax({
       type: 'POST',
       url: '/user/login',
       data: {assertion: assertion},
       success: function(res, status, xhr) { window.location.reload(); },
       error: function(xhr, status, err) {
         navigator.id.logout();
         alert("Login failure: " + err);
       }
     });
   },

   _onlogout: function() {
     // FIXME: Don't hardcode URL.
     this.sandbox.jQuery.ajax({
       type: 'GET',
       url: '/user/_logout',
       success: function(res, status, xhr) { window.location.reload(); },
       error: function(xhr, status, err) {
         navigator.id.logout();
         alert("Logout failure: " + err);
       }
     });
   }


  };
});
