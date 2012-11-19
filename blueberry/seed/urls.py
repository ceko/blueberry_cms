from django.conf.urls import patterns, url


urlpatterns = patterns('blueberry.seed.views',
    url(r'^(?P<path>.*)select-new-block-template/(?P<panel_id>.*)$', 'select_new_block_template', name='select_new_block_template'),
    url(r'^(?P<path>.*)add-block-by-template/(?P<template_id>.*)/(?P<panel_id>.*)/$', 'add_block_by_template', name='add_block_by_template'),    
    url(r'^(?P<path>.*)add-block-success/$', 'add_block_success', name='add_block_success'), 
    url(r'^(?P<path>.*)edit-block/(?P<block_id>.*)/$', 'edit_block', name='edit_block'),
    url(r'^(?P<path>.*)edit-block-success/$', 'edit_block_success', name='edit_block_success'),
    url(r'^(?P<path>.*)delete-block/(?P<block_id>.*)/$', 'delete_block', name='delete_block'),
)


