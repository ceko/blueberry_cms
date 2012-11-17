import os.path


PACKAGE_ROOT = "/".join(os.path.realpath(__file__).split('/')[:-1]) + "/"
TEMPLATE_DIRS = (PACKAGE_ROOT + 'templates/', )
PIPELINE_CSS = { 'core' : {
                    'source_filenames': (
                        'css/base.css',
                        'css/theme.less',
                    ),
                    'output_filename': 'css/core.css',
                }
}
PIPELINE_JS = { 'jquery' : {
                    'source_filenames': (
                        'js/jquery-1.7.1.min.js',
                        #ui stuff or plugins will go here                                                                       
                    ),
                    'output_filename': 'js/core.js',
                },
                'core' : {
                    'source_filenames': (                        
                        'js/base.coffee',                                                
                    ),
                    'output_filename': 'js/core.js',
                }
}  