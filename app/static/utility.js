/* utility.js */
// =================================================================================================
//                              utility methods
// =================================================================================================
// http://stackoverflow.com/a/4256130/72668
String.prototype.format = function () {
    var formatted = this, i;

    for (i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};
String.prototype.hashCode = function () {
    //http://stackoverflow.com/a/7616484/72668
    var hash = 0, i, chr, len;
    if (this.length == 0) return hash;
    for (i = 0, len = this.length; i < len; i++) {
        chr = this.charCodeAt(i);
        hash = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
};

String.prototype.replaceAll = function (search, replace) {
    if (replace === undefined) {
        return this.toString();
    }
    return this.split(search).join(replace);
};

if (typeof console == "undefined") {

    // http://stackoverflow.com/a/13817235
    this.console = {
        log: function () {
        }

    };
}

RegExp.escape = function (str) {
    var specials = /[.*+?|()\[\]{}\\$^]/g; // .*+?|()[]{}\$^
    return str.replace(specials, "\\$&");
};

function numberWithCommas(x) {
    // http://stackoverflow.com/a/2901298/72668
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function cutAtNaturalWordBoundary(text, maxLength) {
    // cut at natural word boundaries
    var lastPunct = 0;

    if (text.length > maxLength) {
        for (var x = 0; x < text.length; x++) {
            if (x > maxLength) {
                text = text.slice(0, lastPunct + 1) + '...';
                break;
            }
            if (";.,)]! ".indexOf(text[x]) != -1) {
                lastPunct = x;
            }
        }
    }
    return text;
}
// http://stackoverflow.com/a/8897628/72668
jQuery.expr.filters.offscreen = function(el) {
    return (
        (el.offsetLeft + el.offsetWidth) < 0 
        || (el.offsetTop + el.offsetHeight) < 0
        || (el.offsetLeft > window.innerWidth || el.offsetTop > window.innerHeight)
    );
};

// http://stackoverflow.com/a/7228322/72668
function randomIntFromInterval(min,max)
{
    return Math.floor(Math.random()*(max-min+1)+min);
}