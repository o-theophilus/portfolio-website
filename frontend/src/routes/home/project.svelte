<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Content from '$lib/comp/content.svelte';
	import Fluid from '$lib/fluid/fluid.svelte';
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

	let intersecting = false;
	onMount(() => {
		if (browser) {
			let ob = new IntersectionObserver(
				(entries) => {
					intersecting = entries[0].isIntersecting;
				},
				{
					threshold: 0.9
				}
			);

			ob.observe(document.querySelector('.project-block'));
		}
	});

	let fluid_op = {
		SIM_RESOLUTION: 32, //128
		DYE_RESOLUTION: 32, //1024
		CAPTURE_RESOLUTION: 256, //512
		DENSITY_DISSIPATION: 1,
		VELOCITY_DISSIPATION: 0.1, //0.3
		PRESSURE: 0.8,
		PRESSURE_ITERATIONS: 20,

		CURL: 0.1, //30
		SPLAT_RADIUS: 1, //0.35
		SPLAT_FORCE: 6000,

		SHADING: true,
		COLORFUL: true,
		COLOR_UPDATE_SPEED: 10,
		PAUSED: false,

		BACK_COLOR: { r: 0, g: 0, b: 0 },
		TRANSPARENT: true,

		BLOOM: false,
		BLOOM_ITERATIONS: 8,
		BLOOM_RESOLUTION: 256,
		BLOOM_INTENSITY: 0.8,
		BLOOM_THRESHOLD: 0.6,
		BLOOM_SOFT_KNEE: 0.7,

		SUNRAYS: false,
		SUNRAYS_RESOLUTION: 196,
		SUNRAYS_WEIGHT: 1.0
	};
</script>

<svelte:window
	on:scroll={(e) => {
		pos.a = set_pos(scroller.a);
		// pos.b = set_pos(scroller.b);
	}}
/>

<section bind:this={section} class:intersecting>
	<div class="sticky" bind:this={sticky}>
		<div class="fluid">
			<Fluid {...fluid_op} />
		</div>

		<Content>
			<div class="project-block" bind:this={block}>
				<strong class="big title"> Project{projects.length > 1 ? 's' : ''} </strong>

				<div class="scroller" style:right="{pos.a}px" bind:this={scroller.a}>
					{#each projects as post}
						<ItemBox
							parent={block}
							{post}
							post_type="project"
							on:ok={() => {
								active_post = post;
							}}
						/>
					{/each}
					<Scroller href="/project"
						>view
						<br />
						more</Scroller
					>
				</div>

				<div class="desc">
					{#key active_post.slug}
						<div in:fade={{ delay: 0, duration: 1000, easing: cubicInOut }}>
							<strong class="large">
								{active_post.title}
							</strong>
							<br />
							{active_post.description}
						</div>
					{/key}
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
	.intersecting {
		background-color: unset;
	}
	.fluid {
		position: absolute;
		/* opacity: 0;
		transition: opacity var(--animTime3);
		transition-timing-function: ease-in-out; */
	}
	/* .intersecting .fluid {
		opacity: 1;
	} */
	.title {
		font-size: 30px;
		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.intersecting .title {
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

		pointer-events: none;
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
		display: flex;
		justify-content: center;
		align-items: center;

		text-align: center;
		position: relative;
	}

	.large {
		font-size: large;
	}
</style>
