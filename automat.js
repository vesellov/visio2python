

debug.log('import automat.js');

function Class() {
}

Class.prototype.construct = function() {};

Class.extend = function(def) {
    var classDef = function() {
        if (arguments[0] !== Class) {
            this.construct.apply(this, arguments);
        }
    };

    var proto = new this(Class);
    var superClass = this.prototype;

    for (var n in def) {
        var item = def[n];                      
        if (item instanceof Function)
            item.$ = superClass;
        proto[n] = item;
    }

    classDef.prototype = proto;

    classDef.extend = this.extend;      
    return classDef;
};


var Automat = Class.extend({

    state: null,

    name: null,

    construct: function(begin_state) {
        this.state = begin_state;
        this.name = "undefined";
        debug.log('CREATED AUTOMAT ' + this.name)
        this.init();
    },

    A: function (event, args) {
    },
    
    init: function () {
    },
    
    state_changed: function (old_state, new_state, event, args) {
    },

    event: function (evt, args) {
        debug.log(this.name + '(' + this.state + ') fired with \'' + evt + '\'');
        var old = this.state;
        this.A(evt, args);
        if (old != this.state)
            debug.log(this.name + ' : ' + old + ' -> ' + this.state);
        	this.state_changed(old, this.state, evt, args);
    }
    
});
