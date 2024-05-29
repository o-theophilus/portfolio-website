<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Content from '$lib/content.svelte';
	import Fluid from './page.3_fluid.svelte';
	import ItemBox from './page.3_post.item_box.svelte';
	import Scroller from '$lib/scroller.svelte';

	let sticky;
	let block;
	let section;
	let scroller = {};
	let pos = {};

	export let projects = [];
	let active_post = projects.length > 0 ? projects[0] : {};

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
		SIM_RESOLUTION: 8, //128
		DYE_RESOLUTION: 64, //1024
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
		<!-- <div class="fluid">
			<Fluid {...fluid_op} />
			<div class="blocker" />
		</div> -->

		<Content>
			<div class="project-block" bind:this={block}>
				<strong class="big title"> Project{projects.length > 1 ? 's' : ''} </strong>

				<div class="scroller" style:right="{pos.a}px" bind:this={scroller.a}>
					{#each projects as post}
						<ItemBox
							parent={block}
							{post}
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
							<strong class="big color1">
								{active_post.title}
							</strong>
							<br />
							{active_post.description}
						</div>
					{/key}
				</div>
			</div>
		</Content>
	</div>
</section>

<style>
	section {
		position: relative;
		height: 300vh;
		/* background-color: var(--ac4);
		
		transition: all var(--animTime3);
		transition-timing-function: ease-in-out; */
	}
	/* .intersecting {
		background-color: unset;
	} */
	.fluid {
		position: absolute;
		/* opacity: 0;
		transition: opacity var(--animTime3);
		transition-timing-function: ease-in-out; */
	}
	/* .intersecting .fluid {
		opacity: 1;
	} */
	.blocker {
		position: absolute;
		inset: 0;
		background-color: var(--ac4);
		pointer-events: none;
		transition: background-color var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.intersecting .blocker {
		background-color: transparent;
	}
	.title {
		font-size: 30px;
		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.intersecting .title {
		font-size: 40px;
		color: var(--ac1);
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
		gap: var(--sp5);
		width: fit-content;

		padding-right: var(--sp5);
	}
	/* .left {
		align-self: flex-end;
		padding: 0;
		padding-left: var(--sp5);
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
</style>
