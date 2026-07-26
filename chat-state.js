const STORAGE_KEY = 'aichat_config';
const PARAMS_KEY = 'aichat_params';
const CONV_KEY = 'aichat_conversations';
const CUR_KEY = 'aichat_current';

let config;
let params;
let messages;
let loading = false;
let currentConvId = null;

let _msgId = 0;
function nextId() { return ++_msgId; }
function findMsg(mid) { return messages.findIndex(m => m._id === mid); }

let _idb = null;
let _idbP = null;
