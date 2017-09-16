const assert = require("chai").assert;
const title_parser = require("../public/client_javascript/title_parser");

describe('Title parser', function() {
    describe('guessTitle() should split artist and song-title for ', function() {
        it('simple titles with -', function() {
            const answer = title_parser.guessTitle("Hello - something");
            assert.equal(answer[0], "Hello");
            assert.equal(answer[1], "something");
        });
        it('japanese titles with /', function() {
            const answer = title_parser.guessTitle("KANABOON / ないものねだり");
            assert.equal(answer[0], "KANABOON");
            assert.equal(answer[1], "ないものねだり");
        });
        it('japanese titles with ／ (different backslash)', function() {
            const answer = title_parser.guessTitle("SAKURA／いきものがかり（Cover）");
            assert.equal(answer[0], "SAKURA");
            assert.equal(answer[1], "いきものがかり（Cover）");
        });
    });
    describe('matchYoutubeLink() should match format of:', function() {
        it('/v/-wtIMTCHWuI', function() {
            const answer = title_parser.matchYoutubeLink("http://www.youtube.com/v/-wtIMTCHWuI");
            assert.notEqual(answer, -1);
        });
        it('.be/-wtIMTCHWuI', function() {
            const answer = title_parser.matchYoutubeLink("http://youtu.be/-wtIMTCHWuI");
            assert.notEqual(answer, -1);
        });
        it('v=-wtIMTCHWuI', function() {
            const answer = title_parser.matchYoutubeLink("http://www.youtube.com/watch?v=-wtIMTCHWuI");
            assert.notEqual(answer, -1);
        });
    });
});
