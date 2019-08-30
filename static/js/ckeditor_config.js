CKEDITOR.editorConfig = function (config) {

    config.language = 'zh-cn';
    config.width = '100%';
    config.height = 400;
    config.toolbarCanCollapse = true;
    config.scayt_autoStartup = false;

    // config.extraPlugins = 'codesnippet,print,format,font,colorbutton,justify,uploadimage';
    config.extraPlugins = 'codesnippet,uploadimage';
    // config.uploadUrl = '/media/';
    config.removePlugins = 'language,elementspath,save,print,scayt';
    // config.toolbar = [
    //     {name: 'clipboard', items: ['Undo', 'Redo']},
    //     {name: 'styles', items: ['Styles', 'Format']},
    //     {
    //         name: 'basicstyles',
    //         items: ['Bold', 'Italic', 'Strike', '-', 'RemoveFormat']
    //     },
    //     {
    //         name: 'paragraph',
    //         items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote']
    //     },
    //     {name: 'links', items: ['Link', 'Unlink']},
    //     {name: 'insert', items: ['Image', 'EmbedSemantic', 'Table', 'EasyImageUpload']},
    //     {name: 'tools', items: ['Maximize']},
    //     {name: 'editing', items: ['Scayt']}
    // ];
};