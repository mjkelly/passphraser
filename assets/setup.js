'use strict;'

// Page setup
document.getElementById('new-btn').addEventListener('click', newPassphrase);
document.getElementById('copy-btn').addEventListener('click', copyPassphrase);
document.getElementById('length').addEventListener('change', newPassphrase);
document.getElementById('separator').addEventListener('change', newPassphrase);

newPassphrase();
