const STORAGE_KEY = 'aichat_config';
const PARAMS_KEY = 'aichat_params';
const CONV_KEY = 'aichat_conversations';

let config;
let params;
let messages;
let loading = false;
let currentConvId = null;

const DEFAULT_MODELS = [
    'deepseek-v4-flash-free',
    'deepseek-chat',
    'gpt-4o',
    'claude-sonnet-4-20250514',
];
let userModels = [];

let _msgId = 0;
function nextId() { return ++_msgId; }
function findMsg(mid) { return messages.findIndex(m => m._id === mid); }

let _idb = null;
let _idbP = null;
