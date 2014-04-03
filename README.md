# Cap'n Proto bindings for Node.js

This package is a somewhat-hacky wrapper around the
[Cap'n Proto](http://capnproto.org) C++ library.  Both the serialization and
the RPC layer are exposed.

This wrapper was created primarily for use in the implementation of
[Sandstorm](http://sandstorm.io), whose frontend is written using
[Meteor](http://meteor.com).

## Installation

### From NPM

    npm install capnp

Note that the C++ part of the module is built during the install process.  Thus,
you must have development headers for Cap'n Proto and Node.js installed, along
with the `node-gyp` tool and a GCC new enough for Cap'n Proto (at least 4.7).
On Debian/Ubuntu, you can install these like so:

    sudo apt-get install nodejs-dev nodejs-legacy capnproto-dev g++

### Form source

    git clone git://github.com/kenton/node-capnp.git
    cd node-capnp
    npm install

Note: node-capnp uses [node-gyp](https://github.com/TooTallNate/node-gyp) for
building. To manually invoke the build process, you can use `node-gyp rebuild`.
This will put the compiled extension in `build/Release/capnp.node`. However,
when you do `require('capnp')`, it will expect the module to be in, for
example, `bin/linux-x64-v8-3.11/capnp.node`. You can manually put the module
here every time you build (or symlink it), or you can use the included build
script. Either `npm install` or `node build -f` will do this for you. If you
are going to be hacking on node-capnp, it may be worthwhile to first do
`node-gyp configure` and then for subsequent rebuilds you can just do
`node-gyp build` which will be faster than a full `npm install` or
`node-gyp rebuild`.

(If the above paragraph looks familiar, it's because it comes from
[node-fibers](http://github.com/laverdet/node-fibers), whose build approach
we copied.)

## Usage

    var capnp = require("capnp");

    // Schemas are parsed at runtime.  import() will search for schemas in:
    // - All node_modules and NODE_PATH directories.
    // - /usr/include and /usr/local/include.
    // (This search strategy is pretty hacky and will probably change in the
    // future.)
    var foo = capnp.import("foo.capnp");

    var obj = capnp.parse(foo.SomeStruct, inputBuffer);
    var outputBuffer = capnp.serialize(foo.SomeStruct, obj);

    // connect() accepts the same address string format as kj::Network.
    var conn = capnp.connect("localhost:1234");

    // restore() is like EzRpc::importCap()
    var cap = conn.restore("exportName", foo.MyInterface);
    
    // Method parameters are native Javascript values, converted using the
    // same rules as capnp.serialize().
    var promise = cap.someMethod("foo", 123, {a: 1, b: 2});

    // Methods return ES6 "Promise" objects.  The response is a Javascript
    // object containing the results by name.
    promise.then(function(response) {
      console.log(response.namedResult);
    });

    // Pipelining is supported.
    promise.anotherMethod();

    // You can explicitly close capabilities and connections if you don't want
    // to wait for the garbage collector to do it.
    cap.close();
    conn.close();

## Caveats

### This implementation is SLOW

Because v8 cannot inline or otherwise optimize calls into C++ code, and because
the C++ bindings are implemented in terms of the "dynamic" API, this
implementation is actually very slow.  In fact, the main advantage of Cap'n
Proto -- the ability to use the wire format as an in-memory format -- does not
apply here, because accessor overhead of such an approach would be too high.
Instead, this implementation is based on decoding messages to native Javascript
objects in an upfront parsing step, and conversely initializing outgoing
messages from complete Javascript objects.  This actually makes the library
somewhat nicer syntactically than it would be otherwise, but it is not fast.


A pure-Javascript implementation would likely be much faster.  See
[capnproto-js](https://github.com/jscheid/capnproto-js) for a nascent such
implementation.  Unfortunately, that implementation is incomplete and does not
support RPC at all.  Hence, this hack was created for short-term use.

Eventually, we expect to replace this implementation with a pure-Javascript
implementation, or perhaps a hybrid that at least has inlinable accessors and
avoids runtime string map lookups.

### The interface is not final

Especially because of the above caveat, we expect the interface may change
in the future.
