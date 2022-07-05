export let posts = [
	{
		title: 'How I met Svelte',
		summary: 'The new reactive component based approach to web design without a virtual DOM.',
		image: 'how-i-met-svelte-01.jpg',
		date: '18 May 2021',
		slug: 'how-i-met-svelte',
		tags: 'Programming',
		type: 'md',
		content: `
Web designing can be a tedious, repetitive and uninteresting process, especially for the fact that it is ever-evolving. A technology you decide to learn today might become obsolete tomorrow with a better tool replacing it.

I have been in search for better approach to web development as existing methods are not intuitive, complex and have a steep learning curve. I found many temples engines – Wix, Webflow DreamWeaver, Blue Griffon, WordPress - and libraries - Angular, React, jQuery, C# with Razor. Most of which will get the job done. But you will always run into issues when trying to fix a small bug or modify/add a custom feature. The source code is usually filled unnecessary and unused codes which will definitely be a nightmare to go through.

I came across this blog: [*Best Frontend Frameworks of 2021 for Web Development*](https://www.simform.com/best-frontend-frameworks/#section9). The blog listed the top 9 frontend frameworks according to various features. That was the first time I ever came across Svelte. Guess what? Svelte was not among the top 5 frameworks on the list. In fact it was last. But the outlined features caught my attention. Especially for that fact that it was the newest on the list at the time and lightweight.

I did a little research and found the maker of Svelte was an average looking man, Rich Harris, who was a graphics editor for New York Time.

Really! A graphic designer. Well, I could relate because at the moment I also work as a graphic designer, but I know deep down I should be programming big time.

I was still sceptical but after watching this great talk by Rich Harris about [rethinking how we build frontend JavaScript frameworks](https://www.youtube.com/watch?v=AdNJ3fydeao), I was sold. If you have half an hour to kill and haven't seen it, please check it out. I promise it is better than any content you will find on my blog.

Svelte is a new reactive component-based approach to web design. Svelte works differently by putting the work into a compile step instead of putting them in the browser, unlike frameworks like React and Vue. It does many other things easily and improves most of the bottlenecks of using other frameworks.

Svelte is “a compiler that takes your declarative components and converts them into efficient JavaScript that surgically updates the DOM” when the state of your application changes. Meaning, you can build boilerplate-free components using CSS, HTML and pure JavaScript, and Svelte will compile it into small and lightweight JS with built-in reactivity.

Visiting the official website of [Svelte](https://svelte.dev/) and [SvelteKit](https://kit.svelte.dev/), It is clearly seen that they are well documented and have good examples.

At this point my palms are sweaty, knees weak, arms are heavy, I was ready to ~get my hands wet~ dive in head first and hope for the best.

I lunched VS Code - the one IDE to rule them all, opened the node terminal and with three lines of code in less than one minute I was able to get my first Svelte web app up and running. My mind was blown, this must be sorcery. Never seen anything like it.


![if you are reading this it was made with Svelte](/images/how-i-met-svelte-02.jpg)

And the rest is history.

I would recommend Svelte if you are:

1. New in web development, lucky you. You will not have to through the pain of unlearning React😊.
2. A veteran in web development, you'll realize how easy life can be.
`
	},
	{
		title: 'Starting your first Svelte App with just 3 lines of code',
		summary: 'This post is intended to demonstrate how easy it is for anyone to create a web app in Svelte.',
		image: 'creating-your-first-svelte-app-01.jpg',
		date: '24 May 2021',
		slug: 'starting-your-first-svelte-app',
		tags: 'Programming',
		type: 'md',
		content: `
\`\`\`node
npm init svelte@next
npm i
npm run dev
\`\`\`

Thats it! Thats all you need to know to get your app started.

All you need now is:
1. An interpreter to process the command.
1. A terminal to type in the commands.

<br>

### The Interpreter
The commands starting with 'npm' are Node command. **Node** is very powerful tool that will help us install, run and build our web app.
1. Download the latest version here: https://nodejs.org/en/download/
![VSCode](/images/creating-your-first-svelte-app-03.jpg)

1. Install Node
> This should be a seamless process

<br>

### The Terminal
The terminal we will be using to type our code is **Visual Studio Code**. VS Code is not just a terminal, it is a very powerful IDE that can easily be extended.
1. Download the latest version here: https://code.visualstudio.com/
![VSCode](/images/creating-your-first-svelte-app-02.jpg)

1. Install VS Code.
	> This should be a seamless process
1. Install "Svelte for VS Code" Extension (Optional).
	> Although not required to get your app started, This Extension will later come in handy when we start coding our web app.
	![VSCode](/images/creating-your-first-svelte-app-09.jpg)
	1. Click on Extensions on the side bar
	1. Search for "Svelte for VS Code"
	1. Select it in the search result
	1. Click on Install
	
	> This extension adds great features to VS Code like: code highlighting, code completion, code formatting, error linting and many more.

<br>

## Lets get started
1. Create a new folder for your project
1. Open VS Code
1. In VS Code, open the folder you created 
![VSCode](/images/creating-your-first-svelte-app-04.jpg)
1. Open the terminal window 
![VSCode](/images/creating-your-first-svelte-app-05.jpg)

1. Type in the first command and press Enter
\`\`\`node
npm init svelte@next
\`\`\`
You will be prompted with some questions. Answers according to the image below.
![VSCode](/images/creating-your-first-svelte-app-07.jpg)
This will scaffold a new project in the folder you created.<br>
![VSCode](/images/creating-your-first-svelte-app-06.jpg)

1. Type in the second command and press Enter
\`\`\`node
npm i
\`\`\`
This is the short form of 'npm install'. This will install your app dependencies.

1. Type in the third command, and press Enter
\`\`\`node
npm run dev
\`\`\`
This will start a development server on 'localhost:3000'.

1. Open your browser and type 'localhost:3000' in the address bar
![VSCode](/images/creating-your-first-svelte-app-08.jpg)

<br>

### Viola!!!
You did it!

You have just created your first working Svelte app. This is the beginning of greater things to come.

What you have created is a skeletal project which is the most basic form of a Svelte app.
This app can be expanded into an extremely high-performance web app. 

<br>

You can learn more and get more details at [Svelte](https://svelte.dev/) and [SvelteKit](https://kit.svelte.dev/).
`
	},
	{
		title: 'Basic Svelte App',
		summary: 'Introduction to basic svelte component and routing.',
		image: 'creating-your-first-svelte-app-01.jpg',
		date: '08 June 2021',
		slug: 'basic-svelte-app',
		tags: 'Programming',
		type: 'md',
		content: `
### Content
1. [Introduction](#introduction)
1. [Svelte folder structure](#svelte-folder-structure)
1. [Starting Svelte app](#starting-svelte-app)
1. [Svelte component](#svelte-component)
1. [Adding a component](#adding-a-component)
1. [Layout component](#layout-component)
1. [Conclusion](#conclusion)

### Introduction

The purpose of this post is to show the basic workflow of svelte and introduce you to some svelte concepts like component and routing.

In this post we will create a svelte app that has a Home page, an About page, and a Contact page.

This post will assume you know how to start a svelte app.

If you are totally new to svelte, you can check out this post on [starting a svelte app](/blog/starting-your-first-svelte-app).


### Svelte folder structure

Once you've gotten you app up and running in VS Code you should have a folder structure that looks something like the image below:

![basic-svelte-app](../images/basic-svelte-app_01.jpg)

Your app is made up of files and folders which includes:

* node_modules - This folder houses all libraries and external modules. You will not have to do anything in this folder.
* src - This folder is where the bulk of your work will be done. This is the root of you app and all your code goes here. Its default contents are:
	* routes - This folder handles the structure and routing of your app,
	* app.html - this is a skeletal html file in which the app will be rendered into,
	* global.d.ts - This is a Type script file. If you are not into TypeScript you can totally ignore this file.
* static - This folder holds all your static files like images, sounds, videos, fonts, etc.
* helper files - This are files that starts with ".", eg. '.eslintrc.cjs'. These files contains settings and help manage your app extensions.
* jsconfig.json and svelte.config.js - This JavaScript files contains the app configurations.
* package-lock.json and package.json - This files contains reference to libraries and and modules that this app depends on.
* README.md -  This is a note written in markdown


### Starting Svelte app

As mentioned earlier, the bulk of the work will be done in the src folder which will be our focus.

Start the default app by running the below code in the \`terminal\`

\`\`\`node
npm run dev
\`\`\`

Open your browser and go to: *localhost:3000*
![VSCode](../images/creating-your-first-svelte-app-08.jpg)

There nothing much going on here, just a welcome page.

The code for this page can be found in \`src/routes/index.svelte\`
\`\`\`html
<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
\`\`\`

### Svelte component
A Svelte component is any file with the \`.svelte\` extension just like our \`index.svelte\` file.
A Svelte component is made up of:
1. Any HTML code, 
1. A script tag -  This contains any JavaScript that controls the behavior of the component, and
1. A style tag - that defines the look and feel of the component, 

Our \`index.svelte\` file contains only HTML code;

This code can be modified to.
\`\`\`html
<h1>This is the Home page</h1>
<p>My name is Theophilus and I am so excited to be creating my first Svelte app</p>
\`\`\`

The good thing about Svelte is that the changes will be seen in the browser realtime.

Let us enhance this component by adding JavaScript to it.

\`\`\`html
<script>
	let name = 'Theophilus';
</script>

<h1>This is the Home page</h1>
<p>My name is {name} and I am so excited to be creating my first Svelte app</p>
\`\`\`

In the code above we simply define a JavaScript variable 'name' and we used this variable within our HTML code.
So whenever we change the value of the 'name' variable the HTML reference changes too

\`\`\`html
<script>
	let name = 'John';
</script>

<h1>This is the Home page</h1>
<p>My name is {name} and I am so excited to be creating my first Svelte app</p>
\`\`\`

We can also style the component.
\`\`\`html
<script>
	let name = 'John';
</script>

<h1>This is the Home page</h1>
<p>My name is {name} and I am so excited to be creating my first Svelte app</p>

<style>
	h1{
		color: red
	}
</style>
\`\`\`

We simply add a red color to the h1 element.

Cool right!!!


### Adding a component

Let us add an "about" component this will serve as the about page the about page.

In the \`src/routes/\` folder create a file and name it \`about.svelte\`.

Input the code below in the component.

\`\`\`html
<h1>This is the About page</h1>
<p>
	This app shows the basic workflow of Svelte and serves as a testing ground for components and routing.
</p>
\`\`\`

We can view this page by going to: *localhost:3000/about* on the browser
![basic-svelte-app](../images/basic-svelte-app_02.jpg)

How cool!!!!


Let's add a "contact" component the same way.
\`\`\`html
<h1>This is the Contact page</h1>
<p>You can reach me on: theophilus.ogbolu@gamil.com</p>
\`\`\`

Again, we can view this page by going to 'localhost:3000/contact'  on the browser

*smile*!!

### Layout component

This is a special component that contains the common components that appears on all pages in the app eg. header, nav and footer.

Create a new fine in the \`src/routes/\` folder, the layout component is a special component and must be named \`__layout.svelte\`

This \`__layout.svelte\` file must contain a \`<slot/>\` tag. This is where the route pages will be rendered.

\`\`\`html
<slot/>
\`\`\`
We can now define the nav bar and footer in this component.

\`\`\`html
<nav>
	<a href="/">Home</a>
	<a href="/about">About</a>
	<a href="/contact">Contact</a>
</nav>

<slot/>

<footer>
	<p>Thank you for visiting my awesome app.</p>
</footer>
\`\`\`

We have a nav element that contain links that navigates to index, about and contact components.

When any of the link is clicked the component is rendered in place of \`<slot />\`.


Let us now style our layout component and add some html element to define the structure of our app

\`\`\`html
<nav>
	<div class="block">
		<a href="/">Home</a>
		<a href="/about">About</a>
		<a href="/contact">Contact</a>
	</div>
</nav>

<section>
	<div class="block">
		<slot />
	</div>
</section>

<footer>
	<div class="block">
		<p>Thank you for visiting my awesome app.</p>
	</div>
</footer>

<style>
	.block {
		max-width: 800px;

		margin: auto;
		padding: 20px 40px;
	}
	nav {
		background-color: bisque;
	}
	section {
		background-color: lightgrey;
	}
	section .block {
		background-color: white;
		min-height: calc(100vh - 210px);
	}

	footer {
		background-color: black;
		color: white;
	}
</style>

\`\`\`


![basic-svelte-app](/images/basic-svelte-app_03.jpg)

### Conclusion

We now have a functional app that contains navigation, styles and a script.

This app can be expanded upon by following the simple process explained in this post.

You can get this project file from the [GitHub Repo](https://github.com/pheezie/basic-svelte-app)
	`
	}
];

export let _posts = [
{
		title: 'Marked Blog',
		summary: 'This is an example of a marked blog',
		image: 'akropol_001.jpg',
		date: '15 May 2021',
		slug: 'test-md-blog',
		tags: 'Programming',
		type: 'md',
		content: undefined
	}
];

export let projects = [
	{
		title: 'Charms Interior Design',
		summary: '',
		image: 'charms_01_01.jpg',
		date: '01 Jan 2021',
		slug: 'charms',
		tags: 'Model, Visualization, Animation',
		type: 'html',
		content: `
			<img class="noDesign" src="/images/charms_01_01.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_02.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_03.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_04.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_05.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_06.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_07.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_08.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_09.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_01_10.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_01.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_02.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_03.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_04.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_05.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_06.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_07.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_08.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_09.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_02_10.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_01.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_02.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_03.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_04.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_05.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_06.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_07.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_08.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_09.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/charms_03_01.jpg" alt="image_image" />
		`
	},

	{
		title: 'Akropol',
		summary: '',
		image: 'akropol_001.jpg',
		date: '01 Jan 2021',
		slug: 'akropol',
		tags: 'Model, Visualization, Animation',
		type: 'html',
		content: `
			<img class="noDesign" src="/images/akropol_001.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/akropol_002.jpg" alt="image_image" />
			<br />
			<br />
			<video controls>
				<source src="/videos/akropol_001.mp4" type="video/mp4" />
			</video>
		`
	},

	{
		title: 'This is Nigeria ft. Falz',
		summary: 'Fan art',
		image: 'tin_001.jpg',
		date: '01 Jan 2021',
		slug: 'this-is-nigeria',
		tags: 'Model, Visualization, Animation',
		type: 'html',
		content: `
			<div class="unit">
				<img class="noDesign" src="/images/tin_001.jpg" alt="image_image" />
				<br />
				<br />
				<video controls>
					<source src="/videos/tin_001.mp4" type="video/mp4" />
				</video>
			</div>
		`
	},
	{
		title: 'Product Viewer - Hummer H3',
		summary: '3D model visualization demo. powered by WebGL',
		image: 'mv_hummer_h3.jpg',
		date: '21 May 2021',
		slug: 'mv-hummer-h3',
		tags: 'Model, Visualization, Animation',
		type: 'md',
		content: `
<iframe
style="width: 100%;
height: 500px;"
src="https://mv-hummer-h3.vercel.app/"
frameborder="0"
title="container"
></iframe>

This is an interactive 3D visualization demo. It aims to illustrate how WebGL offer new ways to showcase and interact with products on the Web.

Since it's running in real-time 3D, you are able to inspect the model from every angle and even interact with various parts.

Modeling, texturing, lightening, rigging and animation was done in Blender. Exporting to WebGL and interaction was done using Verge3D. UI was created using HTML and CSS.

Here is a link to the <a href="/project/l322">first version of this project</a> that was made using Unity3D.

<br>

Interested in hiring me to build something awesome? <span class="link">Get in touch</span>.
		`
	},
	{
		title: 'eInvite',
		summary: 'A customized wedding invite website',
		image: 'eInvite.jpg',
		date: '1 June 2021',
		slug: 'eInvite',
		tags: 'Web',
		type: 'link',
		content: "http://bamianddayo.vercel.app/"
	},
	{
		title: 'Meji',
		summary: 'An eCommerce platform',
		image: 'meji.jpg',
		date: '13 June 2023',
		slug: 'meji',
		tags: 'Web',
		type: 'link',
		content: "http://meji.ng/"
	},
	{
		title: 'Outside (Pre-NFT)',
		summary: 'An algorithm to randomly generate over 10,000 variations of artwork',
		image: 'meji.jpg',
		date: '30 June 2023',
		slug: 'outside',
		tags: 'Web, nft',
		type: 'link',
		content: "http://outside-demo.vercel.app/"
	}
];

export let _projects = [
	{
		title: 'Connekt',
		summary: 'Connekt is a social sharing application that enable users to easily find and connect with other users that are interested in the Products or Services which are being Offered or Requested.',
		image: 'connekt_001.jpg',
		date: '01 Jan 2021',
		slug: 'connekt',
		tags: 'Web',
		type: 'link',
		content: 'http://www.connekt.vercel.app'
	},
	{
		title: 'Lily Collection',
		summary: '',
		image: 'lilyCollection_001.jpg',
		date: '01 Jan 2021',
		slug: 'lily',
		tags: 'Logo, Banner',
		type: 'html',
		content: `
			<img class="noDesign" src="/images/lilyCollection_001.jpg" alt="image_image" />
			<br />
			<br />
			<img class="noDesign" src="/images/lilyCollection_002.jpg" alt="image_image" />
		`
	},
	{
		title: 'Model Viewer - S3V Range Rover L322',
		summary: '',
		image: 'mvS3V.jpg',
		date: '01 Jan 2021',
		slug: 'l322',
		tags: 'Model, Visualization and Animation',
		type: 'html',
		content: `
			<iframe
			title="iframe"
			src="/project/mvS3V/index.html"
			style=" width: 100%; height: 500px; "
			ref="iFrame"/>
		`
	},
	{
		title: 'Interrogation Room',
		summary: '',
		image: 'interrogationRoom_005.jpg',
		date: '01 Jan 2021',
		slug: 'interrogation-room',
		tags: 'Model, Visualization, Animation',
		type: 'html',
		content: `
			<div class="unit">
				<img class="noDesign" src="/images/interrogationRoom_014.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_015.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_016.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_010.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_011.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_008.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_012.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_009.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_013.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_001.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_002.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_003.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_004.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_005.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_006.jpg" alt="image_image" />
				<br />
				<br />
				<img class="noDesign" src="/images/interrogationRoom_007.jpg" alt="image_image" />
			</div>
		`
	},
	{
		title: 'National Identity Management Commission',
		summary: '',
		image: 'nimc_001.jpg',
		date: '01 Jan 2021',
		slug: 'nimc',
		tags: 'Model, Visualization, Animation',
		type: 'html',
		content: `
			<video controls>
				<source src="/videos/nimc_001.mp4" type="video/mp4" />
			</video>
		`
	},
	{
		title: 'Danfo 2.0',
		summary: 'How to rig a Vehicle tutorial.',
		image: 'danfo_001.jpg',
		date: '01 Jan 2021',
		slug: 'danfo',
		tags: 'Model, Visualization, Animation',
		type: 'html',
		content: `
			<div>
				<img class="noDesign" src="/images/danfo_001.jpg" alt="image_image" />
				<br />
				<br />
				<video controls>
					<source src="/videos/danfo_001.mp4" type="video/mp4" />
				</video>
				<br />
				<br />
				<a href="/docs/danfo_001.pdf" class="btn" target="blank">
					Manual
				</a>
			</div>
		`
	},
	{
		title: 'Costar Brochure',
		summary: '',
		image: 'costar_001.jpg',
		date: '01 Jan 2021',
		slug: 'costar',
		tags: 'Brochure',
		type: 'doc',
		content: 'costar_001.pdf'
	},
	{
		title: 'Aris Brochure',
		summary: '',
		image: 'aris_001.jpg',
		date: '01 Jan 2021',
		slug: 'aris',
		tags: 'Brochure',
		type: 'doc',
		content: 'aris_001.pdf'
	}
];
