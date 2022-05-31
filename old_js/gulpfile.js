//1. Make gulpfile
//2. npm i all dependencies
//3. check all folder paths used in gulpfile
//4. Update index.html
//5. Run gulp watch

const sass = require('gulp-sass')(require('sass'));

var gulp = require('gulp'),
    del = require('del'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    print = require('gulp-print'),
    babel = require('gulp-babel');
    // Make sure to include babel-preset-es2015 in the npm installs for the build-js function to work properly.


var CacheBuster = require('gulp-cachebust');
var cachebust = new CacheBuster();

const paths = {
    jsSource: './src/components/**/*.js',
    cssFiles: './src/**/*.css',
    indexFile: './src/index.html',
    scssFiles: './src/**/**/*.scss',
    htmlFiles: './src/**/*.html',
    dist: './src/dist',
};

gulp.task('clean', function (cb) {
    return del([
        'src/dist/**'
    ], cb);
});

gulp.task('build-css', function (cb) {
    gulp.src([paths.scssFiles, paths.cssFiles])
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(cachebust.resources())
        .pipe(concat('styles.css'))
        .pipe(gulp.dest(paths.dist))
        .once('end', cb);
});

gulp.task('build-js', function (cb) {
    gulp.src(['./src/components/**/*.js', './src/components/*.js'])
        .pipe(sourcemaps.init())
        .pipe(babel({
            presets: ['@babel/preset-env']
        }))
        .pipe(concat('bundle.js'))
        //.pipe(uglify())
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest(paths.dist))
        .once('end', cb);
});

// gulp.task('build-html', function () {
//   return gulp.src([paths.htmlFiles, paths.indexFiles])
//     .pipe(gulp.dest(paths.dist))
// });


gulp.task('build', gulp.series("clean", "build-css", "build-js"), function (cb) {
    cb();
});

gulp.task('watch', function () {
    gulp.watch([paths.jsSource[0], paths.cssFiles, paths.scssFiles, '!./src/dist/*'], gulp.series('build'));
});


gulp.task('default', gulp.series('clean', 'watch'), (done) => {
    done();
});
