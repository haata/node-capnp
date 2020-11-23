{
  'targets': [
    {
      'target_name': 'capnp',
      'sources': ['src/node-capnp/capnp.cc'],
      'libraries': ['-lkj', '-lkj-async', '-lcapnp', '-lcapnpc', '-lcapnp-rpc'],
      'cflags_cc': ['-std=c++14'],
      'cflags_cc!': ['-fno-rtti', '-fno-exceptions'],
      'conditions': [
        ['OS=="mac"', {
          'xcode_settings': {
            'OTHER_CPLUSPLUSFLAGS' : ['-std=c++14','-stdlib=libc++'],
            'OTHER_LDFLAGS': ['-stdlib=libc++'],
            'GCC_ENABLE_CPP_RTTI': 'YES',
            'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
            'MACOSX_DEPLOYMENT_TARGET': '10.7'
          },
        }],
        ['OS=="windows"', {
          'include_dirs+': [
            'C:\\ProgramData\\chocolatey\\lib\\capnproto\\tools\\capnproto-c++-0.8.0\\src',
          ],
        }],
        ['OS=="win32"', {
          'include_dirs+': [
            'C:\\ProgramData\\chocolatey\\lib\\capnproto\\tools\\capnproto-c++-0.8.0\\src',
          ],
        }],
        ['OS=="win"', {
          'include_dirs+': [
            'C:\\ProgramData\\chocolatey\\lib\\capnproto\\tools\\capnproto-c++-0.8.0\\src',
          ],
        }],
      ]
    }
  ]
}
