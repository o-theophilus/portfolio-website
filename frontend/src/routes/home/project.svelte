<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	import Content from '$lib/comp/content.svelte';
	// import Fluid from './project_fluid.svelte';
	import ItemBox from './project_item_box.svelte';
	import Scroller from '$lib/comp/scroller.svelte';

	let sticky;
	let block;
	let section;
	let scroller = {};
	let pos = {};

	export let projects = [];
	// export let blogs = [];
	let active_post = projects[0];

	const set_pos = (scroller) =>
		(sticky.offsetTop / (section.clientHeight - sticky.clientHeight)) *
		(scroller.clientWidth - block.clientWidth);

	let in_view = false;
	let show_desc = false;
	onMount(() => {
		if (browser) {
			let ob = new IntersectionObserver(
				(entries) => {
					in_view = entries[0].isIntersecting;
				},
				{
					threshold: 0.9
				}
			);

			ob.observe(document.querySelector('.project-block'));
		}
	});
</script>

<svelte:window
	on:scroll={(e) => {
		pos.a = set_pos(scroller.a);
		// pos.b = set_pos(scroller.b);
	}}
/>

<section bind:this={section} class:in_view>
	<div class="sticky" bind:this={sticky}>
		<!-- <div class="fluid">
			<Fluid />
		</div> -->

		<Content>
			<div class="project-block" bind:this={block}>
				<strong class="big title"> Project{projects.length > 1 ? 's' : ''} </strong>
				
				<div class="scroller" style:right="{pos.a}px" bind:this={scroller.a}>
					{#each projects as post}
						<ItemBox
							{post}
							post_type="project"
							on:mouseenter={() => {
								active_post = post;
								show_desc = true;
							}}
							on:mouseleave={() => {
								show_desc = false;
							}}
						/>
					{/each}
					<Scroller href="/project"
						>view
						<br />
						more</Scroller
					>
				</div>
				
				
				<div class="desc" class:show_desc>
					<strong class="large">
						{active_post.title}
					</strong>
					{active_post.description}
				</div>
				<!-- <br /><br />
				<strong class="big"> Blogs </strong>
				<br />

				<div class="scroller left" style:left="{pos.b}px" bind:this={scroller.b}>
					<Scroller href="/blog"
						>view
						<br />
						more</Scroller
					>
					{#each blogs as post}
						<ItemBox {post} post_type="blog" home />
					{/each}
				</div> -->
			</div>
		</Content>
	</div>
</section>

<style>
	section {
		position: relative;
		height: 300vh;
		background-color: var(--foreground);

		transition: all var(--animTime3);
		transition-timing-function: ease-in-out;
	}
	.in_view {
		background-color: unset;
	}
	/* .fluid {
		opacity: 0;
		transition: opacity var(--animTime3);
		transition-timing-function: ease-in-out;
	}
	.in_view .fluid {
		opacity: 1;
	} */
	.title {
		font-size: 30px;
		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.in_view .title {
		font-size: 40px;
		color: var(--color1);
	}
	
	.sticky {
		position: sticky;
		
		top: 0;
		overflow: hidden;
	}
	.project-block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		height: 100vh;
		/* pointer-events: none; */

	}

	.scroller {
		position: relative;

		display: flex;
		align-items: center;
		gap: var(--gap5);
		width: fit-content;

		padding-right: var(--gap5);
	}
	/* .left {
		align-self: flex-end;
		padding: 0;
		padding-left: var(--gap5);
	} */

	.title,
	.desc {
		height: 30vh;
		/* background-color: yellow; */
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.desc {
		opacity: 0;

		transition: opacity var(--animTime3);
		transition-timing-function: ease-in-out;
	}
	.desc.show_desc {
		opacity: 1;
	}

	.large {
		font-size: large;
	}
</style>
