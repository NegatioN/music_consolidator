const express = require('express');
const router = express.Router();
const { execSync } = require('child_process');
var path = require('path');
var appDir = path.dirname(require.main.filename);

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Music Consolidator' });
});

router.get('/auth', function(req, res, next) {
    res.render('authenticate', { title: 'Music Consolidator Authenticate' });
});

router.get('/metadata/:link', function(req, res, next) {
   var link = req.params.link;
   res.send(get_metadata(link)); 
});

router.post('/signup', function(req,res){
    consolidate_music(req.body.link, req.body.artist, req.body.title);
    res.redirect('/');
});
router.post('/authenticate', function(req,res){
    authenticate(req.body.auth);
    res.redirect('/');
});

function consolidate_music(link, artist, title){
    const cli_call = `python ${appDir}/../../consolidate.py --link \"${link}\" --artist \"${artist}\" --title \"${title}\" --auth \"${appDir}/gmusic.creds\"`;
    console.log(cli_call);
    execSync(cli_call);
}

function authenticate(auth_code){
    const cli_call = `python ${appDir}/../../authenticate.py --code \"${auth_code}\" --path \"${appDir}/gmusic.creds\"`;
    console.log(cli_call);
    execSync(cli_call);
}

function get_metadata(link) {
    const decoded = decodeURIComponent(link)
    const cli_call = `youtube-dl --skip-download -e \"${decoded}\"`;
    const child_process = require('child_process');
    return child_process.execSync(cli_call).toString();
}

module.exports = router;
