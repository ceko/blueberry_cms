import os.path
import urls


PACKAGE_ROOT = "/".join(os.path.realpath(__file__).split('/')[:-1]) + "/"
TEMPLATE_DIRS = (PACKAGE_ROOT + 'templates/', )
PIPELINE_CSS = { 'core' : {
                    'source_filenames': (                        
                        'css/theme.less',
                        'css/colorbox.css',
                    ),
                    'output_filename': 'css/core.css',
                },
                'admin' : {
                    'source_filenames': (
                        'css/admin/edit.less',
                        'css/admin/iframes.less',                      
                    ),
                    'output_filename': 'css/admin.css',
                },
}
PIPELINE_JS = { 'core' : {
                    'source_filenames': (
                        'js/jquery-1.7.1.min.js',
                        'js/jquery.colorbox-min.js',
                        #ui stuff or plugins will go here                                                                       
                    ),
                    'output_filename': 'js/core.js',
                },                
               'edit' : {
                    'source_filenames': (
                        'js/admin/menuwidget.coffee',                        
                        'js/admin/editresource.coffee',                                                                        
                    ),
                    'output_filename': 'js/admin.js',
                }
}  
