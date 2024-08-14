<script>
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Content from '$lib/content.svelte';
	import Link from '$lib/button/link.svelte';
	import Tag from '$lib/button/tag.svelte';
	import Icon from '$lib/icon.svelte';

	let exp = [
		{
			key: 'Wragby',
			name: 'Wragby Business Solutions',
			role: 'Creative Associate',
			date: 'February 2022 - Present',
			exps: [
				'Established and maintained a consistent brand image through the design of a brand identity manual, company profile, and social media profiles.',
				'Led the design of impactful weekly social media content, banners, email templates, and newsletters.',
				'Produced digital and print materials for various mediums, ensuring uniform brand representation, resulting in a 27% increase in brand recognition.'
			],
			tags: ['UI/UX', 'Figma', 'CorelDRAW', 'Photoshop', 'Premiere Pro', 'Illustrator']
		},

		{
			key: 'Astra',
			name: 'Astra',
			role: 'Visual Content Specialist',
			date: 'September 2021 - December 2023',
			exps: [
				'Developed a dynamic webpage using HTML and CSS, implementing prompt engineering for generating distinctive clothing style images via OpenAI.',
				'Utilized the Python Pillow package to create over 10,000 unique NFT images and	metadata.',
				'Integrated Figma for efficient product prototyping, leading to a 33% reduction in design iteration time.',
				'Conducting research and development on training a generative AI model to generate images based on preset images.',
				'Writing scripts to automate the character generation process for Astraverse.'
			],
			tags: [
				'Figma',
				'Illustrator',
				'HTML',
				'CSS',
				'JavaScript',
				'Svelte',
				'Python',
				'Flask',
				'Blender3D',
				// 'Godot',
				'OpenAI',
				'Stable Diffusion',
				'NFT',
				'Game',
				'Unreal Engine'
			]
		},

		{
			key: 'Brandlife',
			name: 'Brandlife Limited',
			role: 'Graphic Designer',
			date: 'August 2019 - February 2022',
			exps: [
				'Collaborated with account managers to design marketing materials for HP, adhering to brand guidelines.',
				'Designed diverse marketing collaterals and presentations for pitches, conducted event center reconnaissance, and designed event center mockups using SketchUp and Blender.',
				'Developed responsive landing pages, resulting in a 15% reduction in campaign execution costs.'
			],
			tags: [
				'CorelDRAW',
				'Photoshop',
				'Illustrator',
				'Premiere Pro',
				'HTML',
				'CSS',
				'JavaScript',
				'React',
				'Blender3D',
				'SketchUp'
			]
		},

		{
			key: 'AI Multi.',
			name: 'AI Multimedia Academy',
			role: 'Graphic Designer',
			date: 'November 2016 - March 2018',
			exps: [
				'Conducted tutoring sessions for students in 3D modeling, animations, and graphic design.',
				'Developed diverse print materials for clients and actively contributed innovative design ideas in brainstorming sessions.'
			],
			tags: ['CorelDRAW', 'Photoshop', 'Illustrator', 'Premiere Pro', 'Blender3D']
		},

		{
			key: 'IZA60',
			name: 'IZA60 Solutions',
			role: 'Graphic / Web Designer Intern',
			date: 'January 2015 - November 2016',
			exps: [
				'Spearheaded a project integrating digital art into advertising campaigns, increasing user engagement by 21%.',
				'Utilized CorelDRAW for crafting logos and designing banners for web advertisements.',
				'Developed websites using HTML and CSS, optimized image sizes with Photoshop, resulting in a 60% improvement in website speed.'
			],
			tags: ['CorelDRAW', 'Photoshop', 'HTML', 'CSS', 'JavaScript']
		}
	];

	let active = 0;

	let devlope = [{ name: 'Verge3D', value: 80 }];
</script>

<Content fit>
	<div class="comp">
		<strong class="ititle dark"> Where I've Worked </strong>
		<br />
		<br />

		<div class="tabs">
			{#each exp as x, i}
				{#if i != 0}
					<div class="line" />
				{/if}
				<div
					class="tab2"
					role="presentation"
					class:active={active == i}
					on:click={() => {
						active = i;
					}}
				>
					<div />
					{x.key}
				</div>
			{/each}
		</div>

		<div class="block">
			<div class="left">
				<div class="indicator">
					<div
						class="pos"
						style:--height="{100 / exp.length}%"
						style:--active="{active * (100 / exp.length)}%"
					/>
				</div>
				<div>
					{#each exp as x, i}
						<div
							role="presentation"
							class="tab"
							class:active={active == i}
							on:click={() => {
								active = i;
							}}
						>
							{x.key}
						</div>
					{/each}
				</div>
			</div>

			<div class="right">
				{#key active}
					<div class="details" in:fade={{ duration: 1000, easing: cubicInOut }}>
						<div class="name">{exp[active].name}</div>
						<div class="role">{exp[active].role}</div>
						<div class="date">{exp[active].date}</div>
						<div class="info">
							<ul>
								{#each exp[active].exps as x}
									<li>{x}</li>
								{/each}
							</ul>
						</div>
						<div class="tags">
							{#each exp[active].tags as x}
								<Tag no_grow>{x}</Tag>
							{/each}
						</div>
					</div>
				{/key}
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
		margin: var(--sp5) 0;
	}

	.block {
		display: flex;
		gap: var(--sp3);
	}

	.left {
		display: none;
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

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}

	li::marker {
		color: var(--cl1);
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

	.tabs {
		--size: 20px;
		display: flex;
		align-items: center;

		height: 40px;
		margin-bottom: var(--sp3);
	}

	.tabs .line {
		background-color: var(--ft2);
		height: 1px;
		width: 100%;
	}

	.tabs .tab2 {
		display: flex;
		justify-content: center;
		align-items: center;

		flex-shrink: 0;
		width: var(--size);
		height: var(--size);
		border-radius: 50%;
		overflow: hidden;

		cursor: pointer;
		outline: 1px solid var(--ft2);
		color: transparent;
		font-size: 0;

		transition: width var(--trans), height var(--trans), border-radius var(--trans),
			padding var(--trans), color var(--trans);
	}

	.tabs .tab2 div {
		border-radius: 50%;
		width: 0;
		height: 0;
		background-color: transparent;
		transition: width var(--trans), height var(--trans), background-color var(--trans);
	}

	.tabs .tab2.active {
		width: unset;
		height: unset;
		padding: var(--sp1) var(--sp3);
		border-radius: var(--sp0);
		font-size: 0.8rem;
		color: var(--ft1);
	}

	.tabs .tab2:not(.active):hover {
		width: calc(1.2 * var(--size));
		height: calc(1.2 * var(--size));
	}
	.tabs .tab2:not(.active):hover div {
		width: calc(0.5 * var(--size));
		height: calc(0.5 * var(--size));
		background-color: var(--ft2);
	}

	@media screen and (min-width: 500px) {
		.tabs {
			display: none;
		}

		.left {
			display: flex;
		}
	}
</style>
