<script>
	import { fly, fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Content from '$lib/content.svelte';
	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
	import Group from './exp.group.svelte';

	let tabs = ['Wragby', 'Astra', 'Brandlife', 'AI Multi.', 'IZA60', 'Dev Exp.', 'Design Exp.'];
	let active = 0;

	let devlope = [
		{ name: 'HTML', value: 95 },
		{ name: 'CSS', value: 90 },
		{ name: 'JavaScript', value: 65 },
		{ name: 'React', value: 50 },
		{ name: 'Svelte', value: 87 },
		{ name: 'Python', value: 90 },
		{ name: 'Flask', value: 85 },
		{ name: 'Postgres', value: 65 }
	];

	let design = [
		{ name: 'Figma', value: 80 },
		{ name: 'CorelDRAW', value: 94 },
		{ name: 'Photoshop', value: 79 },
		{ name: 'Premiere Pro', value: 53 },
		{ name: 'Blender 3D', value: 80 },
		{ name: 'Verge3D', value: 80 },
		{ name: 'SketchUp', value: 85 },
		{ name: 'Godot', value: 30 }
	];
</script>

<Content fit>
	<div class="comp">
		<strong class="ititle dark"> Where I've Worked </strong>
		<br />
		<br />

		<div class="block">
			<div class="left">
				<div class="indicator">
					<div
						class="pos"
						style:--height="{100 / tabs.length}%"
						style:--active="{active * (100 / tabs.length)}%"
					/>
				</div>
				<div>
					{#each tabs as tab, i}
						<div
							role="presentation"
							class="tab"
							class:active={active == i}
							on:click={() => {
								active = i;
							}}
						>
							{tab}
						</div>
					{/each}
					<!-- <div class="tab">get Resume</div> -->
				</div>
			</div>

			<div class="right">
				{#if active == 0}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<div class="name">Wragby Business Solutions</div>
						<div class="role">Creative Associate</div>
						<div class="date">February 2022 - Present</div>
						<div class="info">
							<ul>
								<li>
									Established and maintained a consistent brand image through the design of a brand
									identity manual, company profile, and social media profiles.
								</li>
								<li>
									Led the design of impactful weekly social media content, banners, email templates,
									and newsletters.
								</li>
								<li>
									Produced digital and print materials for various mediums, ensuring uniform brand
									representation, resulting in a 27% increase in brand recognition.
								</li>
							</ul>
						</div>
					</div>
				{:else if active == 1}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<div class="name">Astra</div>
						<div class="role">Visual Content Specialist</div>
						<div class="date">September 2021 - December 2023</div>
						<div class="info">
							<ul>
								<li>
									Developed a dynamic webpage using HTML and CSS, implementing prompt engineering
									for generating distinctive clothing style images via OpenAI.
								</li>
								<li>
									Utilized the Python Pillow package to create over 10,000 unique NFT images and
									metadata.
								</li>
								<li>
									Integrated Figma for efficient product prototyping, leading to a 33% reduction in
									design iteration time.
								</li>
							</ul>
						</div>
					</div>
				{:else if active == 2}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<div class="name">Brandlife Limited</div>
						<div class="role">Graphic Designer</div>
						<div class="date">August 2019 - February 2022</div>
						<div class="info">
							<ul>
								<li>
									Collaborated with account managers to design marketing materials for HP, adhering
									to brand guidelines.
								</li>
								<li>
									Designed diverse marketing collaterals and presentations for pitches, conducted
									event center reconnaissance, and designed event center mockups using SketchUp and
									Blender.
								</li>
								<li>
									Developed responsive landing pages, resulting in a 15% reduction in campaign
									execution costs.
								</li>
							</ul>
						</div>
					</div>
				{:else if active == 3}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<div class="name">AI Multimedia Academy</div>
						<div class="role">Graphic Designer</div>
						<div class="date">November 2016 - March 2018</div>
						<div class="info">
							<ul>
								<li>
									Conducted tutoring sessions for students in 3D modeling, animations, and graphic
									design.
								</li>
								<li>
									Developed diverse print materials for clients and actively contributed innovative
									design ideas in brainstorming sessions.
								</li>
							</ul>
						</div>
					</div>
				{:else if active == 4}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<div class="name">IZA60 Solutions</div>
						<div class="role">Graphic / Web Designer Intern</div>
						<div class="date">January 2015 - November 2016</div>
						<div class="info">
							<ul>
								<li>
									Spearheaded a project integrating digital art into advertising campaigns,
									increasing user engagement by 21%.
								</li>
								<li>
									Utilized CorelDRAW for crafting logos and designing banners for web
									advertisements.
								</li>
								<li>
									Developed websites using HTML and CSS, optimized image sizes with Photoshop,
									resulting in a 60% improvement in website speed.
								</li>
							</ul>
						</div>
					</div>
				{:else if active == 5}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<Group list={devlope} name="Programming Skills" icon="code" />
					</div>
				{:else if active == 6}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<Group list={design} name="Software Skills" icon="wysiwyg" />
					</div>
				{/if}
			</div>
		</div>
		<br />
		<Link
			href="https://drive.google.com/file/d/17Oznj43Gm_oX_SgKbqa0U9-Hex9X3bFn/view?usp=drive_link"
		>
			<div class="link">
				View Résumé
				<Icon icon="arrow_forward" />
			</div>
		</Link>
	</div>
</Content>

<style>
	.comp {
		margin: var(--sp4) 0;
	}

	.block {
		display: flex;
		gap: var(--sp3);
	}

	.left {
		display: flex;
		height: fit-content;
		flex-shrink: 0;
	}
	.right {
		width: 100%;
	}

	.indicator {
		position: relative;
		background-color: var(--bg2);
		width: 1px;
	}

	.pos {
		position: absolute;
		top: var(--active);
		left: -1px;
		width: 3px;
		height: var(--height);

		background-color: var(--cl1);

		transition: top var(--trans);
	}

	.tab {
		padding: var(--sp2);
		cursor: pointer;
		font-size: 0.8rem;

		transition: color var(--trans), background-color var(--trans);
	}

	.tab.active {
		color: var(--ft1);
		background-color: var(--bg2);
	}

	.tab:hover {
		color: var(--ft1);
		background-color: color-mix(in srgb, var(--cl1), transparent 90%);
	}

	.name {
		color: var(--ft1);
		margin-top: var(--sp1);
	}
	.role {
		font-weight: 800;
		font-size: 1.2rem;
		color: var(--ft1);
	}

	.date {
		margin: var(--sp1) 0;
		font-size: 0.8rem;
	}

	.info {
		margin: var(--sp1) 0;
	}

	li::marker {
		color: var(--cl1);
		/* content: '►'; */
	}

	@media screen and (min-width: 500px) {
		.tab {
			font-size: 1rem;
		}
	}

	.link {
		display: inline-flex;
		align-items: center;
		gap: var(--sp1);
		width: fit-content;
		transition: gap var(--trans);
	}

	.link:hover {
		gap: var(--sp2);
	}
</style>
