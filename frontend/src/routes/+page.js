import { api_url } from '$lib/store.js';

export const load = async ({ fetch }) => {
    // const resp = await fetch(`${api_url}/post`, {
    //     method: 'get',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    // });

    // if (resp.ok) {
    //     const data = await resp.json();
    //     if (data.status == 200) {
    //         return {
    //             // blogs: data.data.blogs,
    //             // projects: data.data.projects,
    //         }
    //     }
    // }

    return {
        projects: [
            {
                "comments": [],
                "content": "```node\nnpm init svelte@next\nnpm i\nnpm run dev\n```\n\nThats it! Thats all you need to know to get your app started.\n\nAll you need now is:\n1. An interpreter to process the command.\n1. A terminal to type in the commands.\n\n<br>\n\n### The Interpreter\nThe commands starting with `npm` are Node command. **Node** is very powerful tool that will help us install, run and build our web app.\n1. Download the latest version here: https://nodejs.org/en/download/\n{#photo}\n\n1. Install Node\n> This should be a seamless process\n\n<br>\n\n### The Terminal\nThe terminal we will be using to type our code is **Visual Studio Code**. VS Code is not just a terminal, it is a very powerful IDE that can easily be extended.\n1. Download the latest version here: https://code.visualstudio.com/\n{#photo}\n![VSCode](/images/creating-your-first-svelte-app-02.jpg)\n\n1. Install VS Code.\n\t> This should be a seamless process\n1. Install \"Svelte for VS Code\" Extension (Optional).\n\t> Although not required to get your app started, This Extension will later come in handy when we start coding our web app.\n    {#photo}\n\t1. Click on Extensions on the side bar\n\t1. Search for \"Svelte for VS Code\"\n\t1. Select it in the search result\n\t1. Click on Install\n\t\n\t> This extension adds great features to VS Code like: code highlighting, code completion, code formatting, error linting and many more.\n\n<br>\n\n## Lets get started\n1. Create a new folder for your project\n1. Open VS Code\n1. In VS Code, open the folder you created \n{#photo}\n1. Open the terminal window \n{#photo}\n\n1. Type in the first command and press Enter\n```node\nnpm init svelte@next\n```\nYou will be prompted with some questions. Answers according to the image below.\n{#photo}\nThis will scaffold a new project in the folder you created.<br>\n{#photo}\n\n1. Type in the second command and press Enter\n```node\nnpm i\n```\nThis is the short form of 'npm install'. This will install your app dependencies.\n\n1. Type in the third command, and press Enter\n```node\nnpm run dev\n```\nThis will start a development server on 'localhost:3000'.\n\n1. Open your browser and type 'localhost:3000' in the address bar\n{#photo}\n\n<br>\n\n### Viola!!!\nYou did it!\n\nYou have just created your first working Svelte app. This is the beginning of greater things to come.\n\nWhat you have created is a skeletal project which is the most basic form of a Svelte app.\nThis app can be expanded into an extremely high-performance web app. \n\n<br>\n\nYou can learn more and get more details at [Svelte](https://svelte.dev/) and [SvelteKit](https://kit.svelte.dev/).",
                "created_at": "2021-05-24T18:12:11",
                "description": "This post is intended to demonstrate how easy it is for anyone to create a web app in Svelte.",
                "format": "markdown",
                "key": "7cb6446b2e364b50a9d1eb3160504758",
                "photos": [
                    "/photo/83cd36bb409c40c7b546ecf091829765.jpg",
                    "/photo/c2a5339222d243d2b30f765db7502a59.jpg",
                    "/photo/f12bade5788e4a23b32e1cee430b08a8.jpg",
                    "/photo/aa84804242cb4f85bf5b7523a2223512.jpg",
                    "/photo/6428857c9c9740858713d5585c9ce034.jpg",
                    "/photo/5724dbfcfe024118b2c075bf04e522ed.jpg",
                    "/photo/2f52bee7a24f41b794aaee8979cc05c0.jpg",
                    "/photo/e564cce772b942b6acd5b098d1677e45.jpg",
                    "/photo/127a9d4387ce43d4a7b47eaf48bca606.jpg"
                ],
                "ratings": [],
                "slug": "starting-your-first-svelte-app-with-just-3-lines-of-code",
                "status": "publish",
                "tags": [
                    "programming",
                    "svelte",
                    "web"
                ],
                "title": "Starting your first Svelte App with just 3 lines of code",
                "type": "blog",
                "videos": []
            },
            {
                "comments": [],
                "content": "Web designing can be a tedious, repetitive and uninteresting process, especially for the fact that it is ever-evolving. A technology you decide to learn today might become obsolete tomorrow with a better tool replacing it.\n\nI have been in search for better approach to web development as existing methods are not intuitive, complex and have a steep learning curve. I found many temples engines \u2013 Wix, Webflow DreamWeaver, Blue Griffon, WordPress - and libraries - Angular, React, jQuery, C# with Razor. Most of which will get the job done. But you will always run into issues when trying to fix a small bug or modify/add a custom feature. The source code is usually filled unnecessary and unused codes which will definitely be a nightmare to go through.\n\nI came across this blog: [*Best Frontend Frameworks of 2021 for Web Development*](https://www.simform.com/best-frontend-frameworks/#section9). The blog listed the top 9 frontend frameworks according to various features. That was the first time I ever came across Svelte. Guess what? Svelte was not among the top 5 frameworks on the list. In fact it was last. But the outlined features caught my attention. Especially for that fact that it was the newest on the list at the time and lightweight.\n\nI did a little research and found the maker of Svelte was an average looking man, Rich Harris, who was a graphics editor for New York Time.\n\nReally! A graphic designer. Well, I could relate because at the moment I also work as a graphic designer, but I know deep down I should be programming big time.\n\nI was still sceptical but after watching this great talk by Rich Harris about [rethinking how we build frontend JavaScript frameworks](https://www.youtube.com/watch?v=AdNJ3fydeao), I was sold. If you have half an hour to kill and haven't seen it, please check it out. I promise it is better than any content you will find on my blog.\n\nSvelte is a new reactive component-based approach to web design. Svelte works differently by putting the work into a compile step instead of putting them in the browser, unlike frameworks like React and Vue. It does many other things easily and improves most of the bottlenecks of using other frameworks.\n\nSvelte is \u201ca compiler that takes your declarative components and converts them into efficient JavaScript that surgically updates the DOM\u201d when the state of your application changes. Meaning, you can build boilerplate-free components using CSS, HTML and pure JavaScript, and Svelte will compile it into small and lightweight JS with built-in reactivity.\n\nVisiting the official website of [Svelte](https://svelte.dev/) and [SvelteKit](https://kit.svelte.dev/), It is clearly seen that they are well documented and have good examples.\n\nAt this point my palms are sweaty, knees weak, arms are heavy, I was ready to ~get my hands wet~ dive in head first and hope for the best.\n\nI lunched VS Code - the one IDE to rule them all, opened the node terminal and with three lines of code in less than one minute I was able to get my first Svelte web app up and running. My mind was blown, this must be sorcery. Never seen anything like it.\n\n> {#photo}\n\nAnd the rest is history.\n\nI would recommend Svelte if you are:\n\n1. New in web development, lucky you. You will not have to through the pain of unlearning React\ud83d\ude0a.\n2. A veteran in web development, you'll realize how easy life can be.",
                "created_at": "2021-05-18T18:12:11",
                "description": "The new reactive component based approach to web design without a virtual DOM.",
                "format": "markdown",
                "key": "a93da85382204c61bd0a97a196374fef",
                "photos": [
                    "/photo/58dc9d46b2eb42989864d0d9f2f2fc1d.jpg",
                    "/photo/50078f89a07a46fdae2455525c3cd54f.jpg"
                ],
                "ratings": [],
                "slug": "how-i-met-svelte",
                "status": "publish",
                "tags": [
                    "svelte",
                    "programming"
                ],
                "title": "How I met Svelte",
                "type": "blog",
                "videos": []
            },
            {
                "comments": [],
                "content": "### Content\n1. [Introduction](#introduction)\n1. [Svelte folder structure](#svelte-folder-structure)\n1. [Starting Svelte app](#starting-svelte-app)\n1. [Svelte component](#svelte-component)\n1. [Adding a component](#adding-a-component)\n1. [Layout component](#layout-component)\n1. [Conclusion](#conclusion)\n\n### Introduction\n\nThe purpose of this post is to show the basic workflow of svelte and introduce you to some svelte concepts like component and routing.\n\nIn this post we will create a svelte app that has a Home page, an About page, and a Contact page.\n\nThis post will assume you know how to start a svelte app.\n\nIf you are totally new to svelte, you can check out this post on [starting a svelte app](/blog/starting-your-first-svelte-app).\n\n\n### Svelte folder structure\n\nOnce you've gotten you app up and running in VS Code you should have a folder structure that looks something like the image below:\n\n{#photo}\n\nYour app is made up of files and folders which includes:\n\n* node_modules - This folder houses all libraries and external modules. You will not have to do anything in this folder.\n* src - This folder is where the bulk of your work will be done. This is the root of you app and all your code goes here. Its default contents are:\n\t* routes - This folder handles the structure and routing of your app,\n\t* app.html - this is a skeletal html file in which the app will be rendered into,\n\t* global.d.ts - This is a Type script file. If you are not into TypeScript you can totally ignore this file.\n* static - This folder holds all your static files like images, sounds, videos, fonts, etc.\n* helper files - This are files that starts with \".\", eg. '.eslintrc.cjs'. These files contains settings and help manage your app extensions.\n* jsconfig.json and svelte.config.js - This JavaScript files contains the app configurations.\n* package-lock.json and package.json - This files contains reference to libraries and and modules that this app depends on.\n* README.md -  This is a note written in markdown\n\n\n### Starting Svelte app\n\nAs mentioned earlier, the bulk of the work will be done in the src folder which will be our focus.\n\nStart the default app by running the below code in the `terminal`\n\n```node\nnpm run dev\n```\n\nOpen your browser and go to: *localhost:3000*\n{#photo}\n\nThere nothing much going on here, just a welcome page.\n\nThe code for this page can be found in `src/routes/index.svelte`\n```html\n<h1>Welcome to SvelteKit</h1>\n<p>Visit <a href=\"https://kit.svelte.dev\">kit.svelte.dev</a> to read the documentation</p>\n```\n\n### Svelte component\nA Svelte component is any file with the \\`.svelte\\` extension just like our `index.svelte` file.\nA Svelte component is made up of:\n1. Any HTML code, \n1. A script tag -  This contains any JavaScript that controls the behavior of the component, and\n1. A style tag - that defines the look and feel of the component, \n\nOur \\`index.svelte\\` file contains only HTML code;\n\nThis code can be modified to.\n```html\n<h1>This is the Home page</h1>\n<p>My name is Theophilus and I am so excited to be creating my first Svelte app</p>\n```\n\nThe good thing about Svelte is that the changes will be seen in the browser realtime.\n\nLet us enhance this component by adding JavaScript to it.\n\n```html\n<script>\n\tlet name = 'Theophilus';\n</script>\n\n<h1>This is the Home page</h1>\n<p>My name is {name} and I am so excited to be creating my first Svelte app</p>\n```\n\nIn the code above we simply define a JavaScript variable 'name' and we used this variable within our HTML code.\nSo whenever we change the value of the 'name' variable the HTML reference changes too\n\n```html\n<script>\n\tlet name = 'John';\n</script>\n\n<h1>This is the Home page</h1>\n<p>My name is {name} and I am so excited to be creating my first Svelte app</p>\n```\n\nWe can also style the component.\n```html\n<script>\n\tlet name = 'John';\n</script>\n\n<h1>This is the Home page</h1>\n<p>My name is {name} and I am so excited to be creating my first Svelte app</p>\n\n<style>\n\th1{\n\t\tcolor: red\n\t}\n</style>\n```\n\nWe simply add a red color to the h1 element.\n\nCool right!!!\n\n\n### Adding a component\n\nLet us add an \"about\" component this will serve as the about page the about page.\n\nIn the \\`src/routes/\\` folder create a file and name it \\`about.svelte\\`.\n\nInput the code below in the component.\n\n```html\n<h1>This is the About page</h1>\n<p>\n\tThis app shows the basic workflow of Svelte and serves as a testing ground for components and routing.\n</p>\n```\n\nWe can view this page by going to: *localhost:3000/about* on the browser\n{#photo}\n\nHow cool!!!!\n\n\nLet's add a \"contact\" component the same way.\n```html\n<h1>This is the Contact page</h1>\n<p>You can reach me on: theophilus.ogbolu@gamil.com</p>\n```\n\nAgain, we can view this page by going to 'localhost:3000/contact'  on the browser\n\n*smile*!!\n\n### Layout component\n\nThis is a special component that contains the common components that appears on all pages in the app eg. header, nav and footer.\n\nCreate a new fine in the \\`src/routes/\\` folder, the layout component is a special component and must be named \\`__layout.svelte\\`\n\nThis \\`__layout.svelte\\` file must contain a \\`<slot/>\\` tag. This is where the route pages will be rendered.\n\n```html\n<slot/>\n```\nWe can now define the nav bar and footer in this component.\n\n```html\n<nav>\n\t<a href=\"/\">Home</a>\n\t<a href=\"/about\">About</a>\n\t<a href=\"/contact\">Contact</a>\n</nav>\n\n<slot/>\n\n<footer>\n\t<p>Thank you for visiting my awesome app.</p>\n</footer>\n```\n\nWe have a nav element that contain links that navigates to index, about and contact components.\n\nWhen any of the link is clicked the component is rendered in place of \\`<slot />\\`.\n\n\nLet us now style our layout component and add some html element to define the structure of our app\n\n```html\n<nav>\n\t<div class=\"block\">\n\t\t<a href=\"/\">Home</a>\n\t\t<a href=\"/about\">About</a>\n\t\t<a href=\"/contact\">Contact</a>\n\t</div>\n</nav>\n\n<section>\n\t<div class=\"block\">\n\t\t<slot />\n\t</div>\n</section>\n\n<footer>\n\t<div class=\"block\">\n\t\t<p>Thank you for visiting my awesome app.</p>\n\t</div>\n</footer>\n\n<style>\n\t.block {\n\t\tmax-width: 800px;\n\n\t\tmargin: auto;\n\t\tpadding: 20px 40px;\n\t}\n\tnav {\n\t\tbackground-color: bisque;\n\t}\n\tsection {\n\t\tbackground-color: lightgrey;\n\t}\n\tsection .block {\n\t\tbackground-color: white;\n\t\tmin-height: calc(100vh - 210px);\n\t}\n\n\tfooter {\n\t\tbackground-color: black;\n\t\tcolor: white;\n\t}\n</style>\n\n```\n\n\n{#photo}\n\n### Conclusion\n\nWe now have a functional app that contains navigation, styles and a script.\n\nThis app can be expanded upon by following the simple process explained in this post.\n\nYou can get this project file from the [GitHub Repo](https://github.com/pheezie/basic-svelte-app)",
                "created_at": "2021-06-08T18:12:11",
                "description": "Introduction to basic svelte component and routing.",
                "format": "markdown",
                "key": "f613d52b823f49c3b0cac7de7ad455b3",
                "photos": [],
                "ratings": [],
                "slug": "basic-svelte-app",
                "status": "publish",
                "tags": [
                    "svelte",
                    "model",
                    "programming",
                    "web"
                ],
                "title": "Basic Svelte App",
                "type": "blog",
                "videos": []
            }
        ],
        blogs: [
            {
                "comments": [],
                "content": "```node\nnpm init svelte@next\nnpm i\nnpm run dev\n```\n\nThats it! Thats all you need to know to get your app started.\n\nAll you need now is:\n1. An interpreter to process the command.\n1. A terminal to type in the commands.\n\n<br>\n\n### The Interpreter\nThe commands starting with `npm` are Node command. **Node** is very powerful tool that will help us install, run and build our web app.\n1. Download the latest version here: https://nodejs.org/en/download/\n{#photo}\n\n1. Install Node\n> This should be a seamless process\n\n<br>\n\n### The Terminal\nThe terminal we will be using to type our code is **Visual Studio Code**. VS Code is not just a terminal, it is a very powerful IDE that can easily be extended.\n1. Download the latest version here: https://code.visualstudio.com/\n{#photo}\n![VSCode](/images/creating-your-first-svelte-app-02.jpg)\n\n1. Install VS Code.\n\t> This should be a seamless process\n1. Install \"Svelte for VS Code\" Extension (Optional).\n\t> Although not required to get your app started, This Extension will later come in handy when we start coding our web app.\n    {#photo}\n\t1. Click on Extensions on the side bar\n\t1. Search for \"Svelte for VS Code\"\n\t1. Select it in the search result\n\t1. Click on Install\n\t\n\t> This extension adds great features to VS Code like: code highlighting, code completion, code formatting, error linting and many more.\n\n<br>\n\n## Lets get started\n1. Create a new folder for your project\n1. Open VS Code\n1. In VS Code, open the folder you created \n{#photo}\n1. Open the terminal window \n{#photo}\n\n1. Type in the first command and press Enter\n```node\nnpm init svelte@next\n```\nYou will be prompted with some questions. Answers according to the image below.\n{#photo}\nThis will scaffold a new project in the folder you created.<br>\n{#photo}\n\n1. Type in the second command and press Enter\n```node\nnpm i\n```\nThis is the short form of 'npm install'. This will install your app dependencies.\n\n1. Type in the third command, and press Enter\n```node\nnpm run dev\n```\nThis will start a development server on 'localhost:3000'.\n\n1. Open your browser and type 'localhost:3000' in the address bar\n{#photo}\n\n<br>\n\n### Viola!!!\nYou did it!\n\nYou have just created your first working Svelte app. This is the beginning of greater things to come.\n\nWhat you have created is a skeletal project which is the most basic form of a Svelte app.\nThis app can be expanded into an extremely high-performance web app. \n\n<br>\n\nYou can learn more and get more details at [Svelte](https://svelte.dev/) and [SvelteKit](https://kit.svelte.dev/).",
                "created_at": "2021-05-24T18:12:11",
                "description": "This post is intended to demonstrate how easy it is for anyone to create a web app in Svelte.",
                "format": "markdown",
                "key": "7cb6446b2e364b50a9d1eb3160504758",
                "photos": [
                    "/photo/83cd36bb409c40c7b546ecf091829765.jpg",
                    "/photo/c2a5339222d243d2b30f765db7502a59.jpg",
                    "/photo/f12bade5788e4a23b32e1cee430b08a8.jpg",
                    "/photo/aa84804242cb4f85bf5b7523a2223512.jpg",
                    "/photo/6428857c9c9740858713d5585c9ce034.jpg",
                    "/photo/5724dbfcfe024118b2c075bf04e522ed.jpg",
                    "/photo/2f52bee7a24f41b794aaee8979cc05c0.jpg",
                    "/photo/e564cce772b942b6acd5b098d1677e45.jpg",
                    "/photo/127a9d4387ce43d4a7b47eaf48bca606.jpg"
                ],
                "ratings": [],
                "slug": "starting-your-first-svelte-app-with-just-3-lines-of-code",
                "status": "publish",
                "tags": [
                    "programming",
                    "svelte",
                    "web"
                ],
                "title": "Starting your first Svelte App with just 3 lines of code",
                "type": "blog",
                "videos": []
            },
            {
                "comments": [],
                "content": "Web designing can be a tedious, repetitive and uninteresting process, especially for the fact that it is ever-evolving. A technology you decide to learn today might become obsolete tomorrow with a better tool replacing it.\n\nI have been in search for better approach to web development as existing methods are not intuitive, complex and have a steep learning curve. I found many temples engines \u2013 Wix, Webflow DreamWeaver, Blue Griffon, WordPress - and libraries - Angular, React, jQuery, C# with Razor. Most of which will get the job done. But you will always run into issues when trying to fix a small bug or modify/add a custom feature. The source code is usually filled unnecessary and unused codes which will definitely be a nightmare to go through.\n\nI came across this blog: [*Best Frontend Frameworks of 2021 for Web Development*](https://www.simform.com/best-frontend-frameworks/#section9). The blog listed the top 9 frontend frameworks according to various features. That was the first time I ever came across Svelte. Guess what? Svelte was not among the top 5 frameworks on the list. In fact it was last. But the outlined features caught my attention. Especially for that fact that it was the newest on the list at the time and lightweight.\n\nI did a little research and found the maker of Svelte was an average looking man, Rich Harris, who was a graphics editor for New York Time.\n\nReally! A graphic designer. Well, I could relate because at the moment I also work as a graphic designer, but I know deep down I should be programming big time.\n\nI was still sceptical but after watching this great talk by Rich Harris about [rethinking how we build frontend JavaScript frameworks](https://www.youtube.com/watch?v=AdNJ3fydeao), I was sold. If you have half an hour to kill and haven't seen it, please check it out. I promise it is better than any content you will find on my blog.\n\nSvelte is a new reactive component-based approach to web design. Svelte works differently by putting the work into a compile step instead of putting them in the browser, unlike frameworks like React and Vue. It does many other things easily and improves most of the bottlenecks of using other frameworks.\n\nSvelte is \u201ca compiler that takes your declarative components and converts them into efficient JavaScript that surgically updates the DOM\u201d when the state of your application changes. Meaning, you can build boilerplate-free components using CSS, HTML and pure JavaScript, and Svelte will compile it into small and lightweight JS with built-in reactivity.\n\nVisiting the official website of [Svelte](https://svelte.dev/) and [SvelteKit](https://kit.svelte.dev/), It is clearly seen that they are well documented and have good examples.\n\nAt this point my palms are sweaty, knees weak, arms are heavy, I was ready to ~get my hands wet~ dive in head first and hope for the best.\n\nI lunched VS Code - the one IDE to rule them all, opened the node terminal and with three lines of code in less than one minute I was able to get my first Svelte web app up and running. My mind was blown, this must be sorcery. Never seen anything like it.\n\n> {#photo}\n\nAnd the rest is history.\n\nI would recommend Svelte if you are:\n\n1. New in web development, lucky you. You will not have to through the pain of unlearning React\ud83d\ude0a.\n2. A veteran in web development, you'll realize how easy life can be.",
                "created_at": "2021-05-18T18:12:11",
                "description": "The new reactive component based approach to web design without a virtual DOM.",
                "format": "markdown",
                "key": "a93da85382204c61bd0a97a196374fef",
                "photos": [
                    "/photo/58dc9d46b2eb42989864d0d9f2f2fc1d.jpg",
                    "/photo/50078f89a07a46fdae2455525c3cd54f.jpg"
                ],
                "ratings": [],
                "slug": "how-i-met-svelte",
                "status": "publish",
                "tags": [
                    "svelte",
                    "programming"
                ],
                "title": "How I met Svelte",
                "type": "blog",
                "videos": []
            },
            {
                "comments": [],
                "content": "### Content\n1. [Introduction](#introduction)\n1. [Svelte folder structure](#svelte-folder-structure)\n1. [Starting Svelte app](#starting-svelte-app)\n1. [Svelte component](#svelte-component)\n1. [Adding a component](#adding-a-component)\n1. [Layout component](#layout-component)\n1. [Conclusion](#conclusion)\n\n### Introduction\n\nThe purpose of this post is to show the basic workflow of svelte and introduce you to some svelte concepts like component and routing.\n\nIn this post we will create a svelte app that has a Home page, an About page, and a Contact page.\n\nThis post will assume you know how to start a svelte app.\n\nIf you are totally new to svelte, you can check out this post on [starting a svelte app](/blog/starting-your-first-svelte-app).\n\n\n### Svelte folder structure\n\nOnce you've gotten you app up and running in VS Code you should have a folder structure that looks something like the image below:\n\n{#photo}\n\nYour app is made up of files and folders which includes:\n\n* node_modules - This folder houses all libraries and external modules. You will not have to do anything in this folder.\n* src - This folder is where the bulk of your work will be done. This is the root of you app and all your code goes here. Its default contents are:\n\t* routes - This folder handles the structure and routing of your app,\n\t* app.html - this is a skeletal html file in which the app will be rendered into,\n\t* global.d.ts - This is a Type script file. If you are not into TypeScript you can totally ignore this file.\n* static - This folder holds all your static files like images, sounds, videos, fonts, etc.\n* helper files - This are files that starts with \".\", eg. '.eslintrc.cjs'. These files contains settings and help manage your app extensions.\n* jsconfig.json and svelte.config.js - This JavaScript files contains the app configurations.\n* package-lock.json and package.json - This files contains reference to libraries and and modules that this app depends on.\n* README.md -  This is a note written in markdown\n\n\n### Starting Svelte app\n\nAs mentioned earlier, the bulk of the work will be done in the src folder which will be our focus.\n\nStart the default app by running the below code in the `terminal`\n\n```node\nnpm run dev\n```\n\nOpen your browser and go to: *localhost:3000*\n{#photo}\n\nThere nothing much going on here, just a welcome page.\n\nThe code for this page can be found in `src/routes/index.svelte`\n```html\n<h1>Welcome to SvelteKit</h1>\n<p>Visit <a href=\"https://kit.svelte.dev\">kit.svelte.dev</a> to read the documentation</p>\n```\n\n### Svelte component\nA Svelte component is any file with the \\`.svelte\\` extension just like our `index.svelte` file.\nA Svelte component is made up of:\n1. Any HTML code, \n1. A script tag -  This contains any JavaScript that controls the behavior of the component, and\n1. A style tag - that defines the look and feel of the component, \n\nOur \\`index.svelte\\` file contains only HTML code;\n\nThis code can be modified to.\n```html\n<h1>This is the Home page</h1>\n<p>My name is Theophilus and I am so excited to be creating my first Svelte app</p>\n```\n\nThe good thing about Svelte is that the changes will be seen in the browser realtime.\n\nLet us enhance this component by adding JavaScript to it.\n\n```html\n<script>\n\tlet name = 'Theophilus';\n</script>\n\n<h1>This is the Home page</h1>\n<p>My name is {name} and I am so excited to be creating my first Svelte app</p>\n```\n\nIn the code above we simply define a JavaScript variable 'name' and we used this variable within our HTML code.\nSo whenever we change the value of the 'name' variable the HTML reference changes too\n\n```html\n<script>\n\tlet name = 'John';\n</script>\n\n<h1>This is the Home page</h1>\n<p>My name is {name} and I am so excited to be creating my first Svelte app</p>\n```\n\nWe can also style the component.\n```html\n<script>\n\tlet name = 'John';\n</script>\n\n<h1>This is the Home page</h1>\n<p>My name is {name} and I am so excited to be creating my first Svelte app</p>\n\n<style>\n\th1{\n\t\tcolor: red\n\t}\n</style>\n```\n\nWe simply add a red color to the h1 element.\n\nCool right!!!\n\n\n### Adding a component\n\nLet us add an \"about\" component this will serve as the about page the about page.\n\nIn the \\`src/routes/\\` folder create a file and name it \\`about.svelte\\`.\n\nInput the code below in the component.\n\n```html\n<h1>This is the About page</h1>\n<p>\n\tThis app shows the basic workflow of Svelte and serves as a testing ground for components and routing.\n</p>\n```\n\nWe can view this page by going to: *localhost:3000/about* on the browser\n{#photo}\n\nHow cool!!!!\n\n\nLet's add a \"contact\" component the same way.\n```html\n<h1>This is the Contact page</h1>\n<p>You can reach me on: theophilus.ogbolu@gamil.com</p>\n```\n\nAgain, we can view this page by going to 'localhost:3000/contact'  on the browser\n\n*smile*!!\n\n### Layout component\n\nThis is a special component that contains the common components that appears on all pages in the app eg. header, nav and footer.\n\nCreate a new fine in the \\`src/routes/\\` folder, the layout component is a special component and must be named \\`__layout.svelte\\`\n\nThis \\`__layout.svelte\\` file must contain a \\`<slot/>\\` tag. This is where the route pages will be rendered.\n\n```html\n<slot/>\n```\nWe can now define the nav bar and footer in this component.\n\n```html\n<nav>\n\t<a href=\"/\">Home</a>\n\t<a href=\"/about\">About</a>\n\t<a href=\"/contact\">Contact</a>\n</nav>\n\n<slot/>\n\n<footer>\n\t<p>Thank you for visiting my awesome app.</p>\n</footer>\n```\n\nWe have a nav element that contain links that navigates to index, about and contact components.\n\nWhen any of the link is clicked the component is rendered in place of \\`<slot />\\`.\n\n\nLet us now style our layout component and add some html element to define the structure of our app\n\n```html\n<nav>\n\t<div class=\"block\">\n\t\t<a href=\"/\">Home</a>\n\t\t<a href=\"/about\">About</a>\n\t\t<a href=\"/contact\">Contact</a>\n\t</div>\n</nav>\n\n<section>\n\t<div class=\"block\">\n\t\t<slot />\n\t</div>\n</section>\n\n<footer>\n\t<div class=\"block\">\n\t\t<p>Thank you for visiting my awesome app.</p>\n\t</div>\n</footer>\n\n<style>\n\t.block {\n\t\tmax-width: 800px;\n\n\t\tmargin: auto;\n\t\tpadding: 20px 40px;\n\t}\n\tnav {\n\t\tbackground-color: bisque;\n\t}\n\tsection {\n\t\tbackground-color: lightgrey;\n\t}\n\tsection .block {\n\t\tbackground-color: white;\n\t\tmin-height: calc(100vh - 210px);\n\t}\n\n\tfooter {\n\t\tbackground-color: black;\n\t\tcolor: white;\n\t}\n</style>\n\n```\n\n\n{#photo}\n\n### Conclusion\n\nWe now have a functional app that contains navigation, styles and a script.\n\nThis app can be expanded upon by following the simple process explained in this post.\n\nYou can get this project file from the [GitHub Repo](https://github.com/pheezie/basic-svelte-app)",
                "created_at": "2021-06-08T18:12:11",
                "description": "Introduction to basic svelte component and routing.",
                "format": "markdown",
                "key": "f613d52b823f49c3b0cac7de7ad455b3",
                "photos": [],
                "ratings": [],
                "slug": "basic-svelte-app",
                "status": "publish",
                "tags": [
                    "svelte",
                    "model",
                    "programming",
                    "web"
                ],
                "title": "Basic Svelte App",
                "type": "blog",
                "videos": []
            }
        ],
        "tags": [
            "model",
            "programming",
            "svelte",
            "web"
        ]
    }
}