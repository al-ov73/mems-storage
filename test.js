import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 5, // Одновременные пользователи
    duration: '15s', // Длительность теста
};

export default function () {
    let res = http.get('https://memovoz.ru/');
    check(res, {
        'is main page status 200': (r) => r.status === 200,
    });
    
    let apiRes = http.get('https://memovoz.ru:8000/memes/checked?skip=0&limit=60');
    check(apiRes, {
        'is API status 200': (r) => r.status === 200,
    });

    console.log(`User: ${__VU}, API TTFB: ${apiRes.timings.wait} ms`);
    console.log(`User: ${__VU}, API Full load time: ${apiRes.timings.duration} ms`);

    sleep(1);
}