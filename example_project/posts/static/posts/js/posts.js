var
  deps = ["ngSanitize", "ngCookies"],
  app = angular.module("django-comments-threaded", deps)
;
app
  .constant("MaxLevel", window.ctf.maxLevel)
  .provider("djangoAjax", [
    function() {
      var
        headerName = "X-CSRFToken",
        xhrHeaderName = "X-Requested-With",
        xhrHeaderValue = "XMLHttpRequest",
        cookieName = "csrftoken"
      ;
      return {
        $get: ["$cookies", function($cookies) {
          return {
            "request": function(config) {
              config.headers[headerName] = $cookies[cookieName];
              config.headers[xhrHeaderName] = xhrHeaderValue;
              return config;
            }
          };
        }
      ]
    };
  }])
  .config(["$interpolateProvider", "$rootScopeProvider", "$httpProvider", "MaxLevel", function($interpolateProvider, $rootScopeProvider, $httpProvider, MaxLevel){
    $httpProvider.interceptors.push("djangoAjax");
    $interpolateProvider.startSymbol("{$");
    $interpolateProvider.endSymbol("$}");
    $rootScopeProvider.digestTtl(50);

  }])
  .filter("nl2br", ["$sanitize", function($sce){
    return function(string){
      return $sce((string + "").replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, "$1<br>$2"));
    };
  }])
  .filter("threadSize", function(){
    return function(comment) {
      return parseInt((comment.rght - comment.lft) / 2);
    };
  })
  .controller("CommentTreeCtrl", ["$scope", "$http", "$log", "MaxLevel", function($scope, $http, $log, MaxLevel){
    $http
      .get(ctf.tree)
      .success(function(tree){
        $scope.tree = tree;
      });

    $scope.replyingTo = null;
    $scope.openedThreads = [];
    $scope.toggleThread = function(comment){
      $scope.openedThreads.push(comment.tree_id);
    }

    $scope.threadSize = function(comment){
      return parseInt((comment.rght - comment.lft) / 2)
    };

    $scope.delete = function(comment){
      $http
        .delete(comment.comment_url)
        .success(function(json){
          $log.info("Successfully deleted")
        })
        .error(function(json){
          $log.info("Error during comment deletion", json)
        })
      ;
    };

    $scope.isShowMore = function(comment){
      return (comment.level >= MaxLevel - 1) &&
             (comment.rght - comment.lft > 1) &&
             ($scope.openedThreads.indexOf(comment.thread_id) == -1);
    }

    $scope.isExpanded = function(comment){
      return (comment.level <  MaxLevel - 1) ||
             ($scope.openedThreads.indexOf(comment.thread_id) != -1);
    }

    $scope.isReplying = function(comment){
      return $scope.replyingTo == comment.id
    }

    $scope.toggleReplyForm = function(comment){
      $scope.replyingTo = $scope.isReplying(comment) ? null : comment.id;
    }

    $scope.reply = function(comment, newComment){
      $http
        .post(comment.comment_url, newComment)
        .success(function(json){
          if (typeof comment.replies == "undefined") {
            comment.replies = []
          }
          comment.replies.push(json);
          $scope.replyingTo = null;
        })
        .error(function(json){
        })
      ;
    };
  }])
  .controller("CommentCreateCtrl", ["$scope", "$http", function($scope, $http){
    $scope.newComment = {};
    $scope.isSubmitting = false;

    $scope.create = function(){
      $scope.isSubmitting = true;
      $http
        .post(ctf.create, $scope.newComment)
        .success(function(json){
          $scope.isSubmitting = false;
          $scope.new_comment = {};
          $scope.$parent.tree.push(json);
        })
        .error(function(json){
          console.log('error', json);
          $scope.isSubmitting = false;
        })
      ;
    }
  }])
;
