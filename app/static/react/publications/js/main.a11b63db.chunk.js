(this["webpackJsonpreact-publications"]=this["webpackJsonpreact-publications"]||[]).push([[0],{13:function(e,t,n){},15:function(e,t,n){},16:function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),s=n(3),c=n.n(s),i=(n(13),n(1)),o=n.n(i),l=n(4),u=n(6),p=n(5),m=n(7),f=function(e){var t=e.label,n=e.publications;return r.a.createElement("section",{className:"container"},r.a.createElement("h2",null,t),r.a.createElement("ul",{className:"list-group"},n.map((function(e){var t=e.links.find((function(e){return"self"===e.rel})),n=e.links.find((function(e){return"delete"===e.rel}));return r.a.createElement("li",{className:"list-group-item d-inline-flex align-items-center"},r.a.createElement("span",{className:"flex-grow-1"},e.title),r.a.createElement("div",{className:"buttons"},t&&r.a.createElement("a",{className:"btn btn-info mr-2",href:t.href},r.a.createElement("i",{class:"fas fa-info-circle"}),r.a.createElement("span",{className:"d-none d-sm-inline ml-1"},"Szczeg\xf3\u0142y")),n&&r.a.createElement("a",{className:"btn btn-danger mr-2",href:n.href},r.a.createElement("i",{class:"fas fa-trash"}),r.a.createElement("span",{className:"d-none d-sm-inline ml-1"},"Usu\u0144"))))}))))},b=(n(15),function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(u.a)(this,Object(p.a)(t).call(this,e))).getCurrentUserLogin=function(){var e,t,a;return o.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return e=new URL("api/login",n.props.urls.clientBase),r.next=3,o.a.awrap(fetch(e));case 3:return t=r.sent,r.next=6,o.a.awrap(t.text());case 6:return a=r.sent,n.setState({login:a}),r.abrupt("return",a);case 9:case"end":return r.stop()}}))},n.getActionList=function(){var e,t;return o.a.async((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,o.a.awrap(fetch(n.props.urls.publicationsApi));case 2:return e=a.sent,a.next=5,o.a.awrap(e.json());case 5:t=a.sent,n.setState({actions:t._links});case 7:case"end":return a.stop()}}))},n.getPublications=function(){var e,t,a,r;return o.a.async((function(s){for(;;)switch(s.prev=s.next){case 0:if(n.state.actions["publications.list"]){s.next=2;break}return s.abrupt("return");case 2:return n.setState({loadingPublications:!0}),e=(e=n.state.actions["publications.list"].href).replace("{user}",n.state.login),t=new URL(e,n.props.urls.publicationsApi),s.next=8,o.a.awrap(fetch(t));case 8:return a=s.sent,s.next=11,o.a.awrap(a.json());case 11:r=s.sent,n.setState({publications:r,loadingPublications:!1});case 13:case"end":return s.stop()}}))},n.componentDidMount=function(){return o.a.async((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,o.a.awrap(n.getCurrentUserLogin());case 2:return e.next=4,o.a.awrap(n.getActionList());case 4:n.getPublications();case 5:case"end":return e.stop()}}))},n.componentDidUpdate=function(){return o.a.async((function(e){for(;;)switch(e.prev=e.next){case 0:case"end":return e.stop()}}))},n.render=function(){return r.a.createElement("div",{className:"App"},r.a.createElement("section",{class:"container text-center px-5 intro"},r.a.createElement("h1",{class:"mt-2"},"Publikacje")),r.a.createElement(f,{label:"Twoje publikacje",publications:n.state.publications}))},n.state={login:null,loadingPublications:!1,publications:[],actions:{}},n}return Object(m.a)(t,e),t}(r.a.Component));Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var d={clientBase:document.getElementById("app-url").innerText,filesApi:document.getElementById("file-api-url").innerText,publicationsApi:document.getElementById("publications-api-url").innerText};c.a.render(r.a.createElement(b,{urls:d}),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))},8:function(e,t,n){e.exports=n(16)}},[[8,1,2]]]);
//# sourceMappingURL=main.a11b63db.chunk.js.map