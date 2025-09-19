import { worker } from "./concurrent";

test('test concurrent', async () => {
    const tasks1 = [
        () => new Promise((resolve) => setTimeout(() => resolve(1), 100)),
        () => new Promise((resolve) => setTimeout(() => resolve(2), 200)),
        () => new Promise((resolve) => setTimeout(() => resolve(3), 300)),
        () => new Promise((resolve) => setTimeout(() => resolve(4), 100)),
        () => new Promise((resolve) => setTimeout(() => resolve(5), 200)),
        () => new Promise((resolve) => setTimeout(() => resolve(6), 300)),
        () => new Promise((resolve) => setTimeout(() => resolve(1), 100)),
        () => new Promise((resolve) => setTimeout(() => resolve(2), 200)),
        () => new Promise((resolve) => setTimeout(() => resolve(3), 300)),
        () => new Promise((resolve) => setTimeout(() => resolve(4), 100)),
        () => new Promise((resolve) => setTimeout(() => resolve(5), 200)),
        () => new Promise((resolve) => setTimeout(() => resolve(6), 300)),
    ];

    // worker(tasks1).then(results => console.log(results))
    // worker(tasks1).then(results => console.log(results))

    let resutls = await Promise.all([worker(tasks1), worker(tasks1)]) 
    console.log(resutls)
});

test('map', async ()=> {
    const execute = (i: any) => { console.log(i); return i }
    const tasks = Array.from({ length: 10 }, (_, i) => async () => {
        return await execute(i);
    });

    let resutls = await Promise.all([worker(tasks), worker(tasks)]) 
    console.log(resutls)
})