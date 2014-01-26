ckan.module('persona', function(jQuery, _) {
  return {
    options: {
      user: null
    },
    initialize: function() {

      jQuery.proxyAll(this, /_on/);

      switch (this.options.action) {
        case "watch":
          // Tell Persona what user is logged in and what functions to call
          // when a user logs in or logs out.
          navigator.id.watch({
            loggedInUser: this.options.user,
            onlogin: this._onlogin,
            onlogout: this._onlogout
          });
          break;
        case "login":
          // This javascript module was called on a login button, attach the
          // on login method to the element.
          this.el.on('click', this._on_login_clicked);
          break;
        case "logout":
          // This javascript module was called on a logout button, attach the
          // on logout method to the element.
          this.el.on('click', this._on_logout_clicked);
          break;
      }
    },

   _on_login_clicked: function() {
     navigator.id.request();
   },

   _on_logout_clicked: function() {
     navigator.id.logout();
   },

   _onlogin: function(assertion) {
     // FIXME: Don't hardcode URLs here.
     this.sandbox.jQuery.ajax({
       type: 'POST',
       url: '/user/login',
       data: {assertion: assertion},
       success: function(res, status, xhr) {
         window.location.replace("/dashboard");
       },
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
