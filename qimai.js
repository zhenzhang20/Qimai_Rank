function C(a, n) {
    a = a["split"]("");
    for (var t = a["length"], e = n["length"], r = "charCodeAt", i = 0; i < t; i++) a[i] = m(a[i][r](0) ^ n[(i + 10) % e][r](0));
    return a["join"]("")
}

function m(n) {
        var t = "fromCharCode";
        return String[t](n)
    }
    //上面是分析f(k)函数
    //下面是f(e)函数
    //函数v(n)就是f（e）函数的结果，m函数和上面的函数一样，只需要分析其中的n_fun函数的实现

function v(n) {
    return n_fun(encodeURIComponent(n)["replace"](/%([0-9A-F]{2})/g,
        function (a, n) {
            return m("0x" + n)
        }))
}

function n_fun(t) {
    var n;
    n = e_from(t.toString(), "binary") ;
    return q_fromByteArray(n) // 这一处的代码相当于 n.toString("base64")
}

function e_from(t_str, b) {
    var r = t_str.length;
    t = new Uint8Array(r);
    var i = t_write(t, t_str, b, r);
    return t
}

function t_write(t, e, b, r) {
    return K(W(e), t, 0, r)
}

function K(t, e, n, r) {
    for (var j = 0; j < r && !(j + n >= e.length || j >= t.length); ++j) e[j + n] = t[j];
    return j
}

function W(t) {
    for (var e = [], n = 0; n < t.length; ++n) e.push(255 & t.charCodeAt(n));
    return e
}
l = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9,+,/"
l = l.split(",")
function q_fromByteArray(t) {

    for (var e, n = t.length,
        r = n % 3,
        i = "",
        o = [], a = 16383, u = 0, c = n - r; u < c; u += a) o.push(s(t, u, u + a > c ? c : u + a));
    return 1 === r ? (e = t[n - 1], i += l[e >> 2], i += l[e << 4 & 63], i += "==") : 2 === r && (e = (t[n - 2] << 8) + t[n - 1], i += l[e >> 10], i += l[e >> 4 & 63], i += l[e << 2 & 63], i += "="),
        o.push(i),
        o.join("")
}

function s(t, e, n) {
    for (var r, i = [], o = e; o < n; o += 3) r = (t[o] << 16 & 16711680) + (t[o + 1] << 8 & 65280) + (255 & t[o + 2]),
        i.push(a(r));
    return i.join("")
}

function a(t) {
    return l[t >> 18 & 63] + l[t >> 12 & 63] + l[t >> 6 & 63] + l[63 & t]
}

function get0analysis(synct, params) {
    var g = new Date() - 1000 * synct;
    var e = new Date() - g - 1515125653845;
    var analy = [];
    var palist = [];
    for (var key in params) {
        palist.push(params[key])
    }
    var mm = palist["sort"]()["join"]("");
    var mmm = v(mm); //参数mm先执行f(e)函数
    var m_str1 = mmm + '@#/rank/indexPlus/brand_id/1@#57313212470@#1';
    var m_str0 = mmm + '@#/rank/indexPlus/brand_id/0@#57313212470@#0';
    var m_str2 = mmm + '@#/rank/indexPlus/brand_id/2@#57313212470@#2';
    var b_str = "00000008d78d46a";
    var r2 = v(C(m_str2, b_str));
    var r0 = v(C(m_str0, b_str));
    var r1 = v(C(m_str1, b_str)) ;
    analy.push(r0, r1, r2);
    return analy
}