import {renderMathCourses} from './render_math.mjs';
for(const report of await renderMathCourses(process.argv.slice(2)))console.log(`Math ${report.course}: ${report.equations} equations / KaTeX ${report.version}`);
