<script>
	import { cubicInOut } from 'svelte/easing';
	import { fade } from 'svelte/transition';

	import { LinkArrow, Tag } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Icon } from '$lib/macro';

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

	let active = $state(0);

	// let devlope = [{ name: 'Verge3D', value: 80 }];
</script>

<Content --content-height="100%" --content-padding-top="80px">
	<div class="page_title dark">Where I've Worked</div>
	<br />

	<div class="block">
		<div class="tab">
			{#each exp as x, i}
				<button
					class:active={active == i}
					onclick={() => {
						active = i;
					}}
				>
					<Icon icon={x.key.toLowerCase()} size={active == i ? '24' : '20'}></Icon>
					<div class="name">
						{x.key}
					</div>
				</button>
			{/each}
		</div>

		<div class="details">
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
							<Tag>
								<img
									class="tag_icon"
									src="/logo/{x.toLowerCase()}.png"
									alt={x}
									onerror={(e) => {
										const img = e.currentTarget;
										img.parentNode && img.parentNode.removeChild(img);
									}}
								/>
								{x}
							</Tag>
						{/each}
					</div>
				</div>
			{/key}
		</div>
	</div>
	<br />
	<LinkArrow href="/Theophilus_Ogbolu_Resume.pdf" blank --link-font-size="0.8rem">
		View Résumé
	</LinkArrow>
</Content>

<style>
	.block {
		display: flex;
		flex-direction: column;
		gap: 24px;
	}

	.tab {
		--size: 32px;
		display: flex;

		border-bottom: 1px solid var(--ol);

		position: relative;

		&::before {
			content: '';

			position-anchor: --active;
			position: absolute;

			bottom: calc(anchor(bottom) - 2px);
			left: anchor(left);
			right: anchor(right);
			height: 3px;

			background-color: var(--cl1);

			transition:
				left 0.2s ease-in-out,
				right 0.2s ease-in-out;
		}

		& button {
			all: unset;
			cursor: pointer;

			display: flex;
			align-items: center;
			gap: 0;

			border-radius: 4px;
			height: 56px;
			padding: 0 16px;
			font-size: 0;
			fill: var(--ft1);
			flex-shrink: 0;

			transition:
				gap 0.2s ease-in-out,
				font-size 0.2s ease-in-out,
				color 0.2s ease-in-out,
				background-color 0.2s ease-in-out;

			&.active {
				anchor-name: --active;

				gap: 8px;
				color: var(--ft1);
				font-size: 0.8rem;
				background-color: var(--bg3);
			}

			&:hover {
				color: var(--ft1);
				background-color: var(--bg2);
			}
		}
	}

	@media screen and (min-width: 500px) {
		.block {
			flex-direction: row;
		}

		.tab {
			flex-direction: column;
			height: fit-content;

			border: none;
			border-left: 1px solid var(--ol);

			&::before {
				top: anchor(top);
				bottom: anchor(bottom);
				left: calc(anchor(left) - 2px);
				width: 3px;
				height: unset;

				transition:
					top 0.2s ease-in-out,
					bottom 0.2s ease-in-out;
			}

			& button {
				gap: 8px;
				font-size: 0.8rem;
			}
		}
	}

	.details {
		width: 100%;

		& .name {
			font-size: 0.8rem;
			margin-top: 8px;
		}
		& .role {
			font-weight: 800;
			font-size: 1.2rem;
			color: var(--ft1);
		}

		& .date {
			margin: 8px 0;
			font-size: 0.7rem;
		}

		& .info {
			margin: 8px 0;

			/* li::marker { */
			/* color: var(--ol); */
			/* } */
		}

		& .tags {
			display: flex;
			flex-wrap: wrap;
			gap: 4px;

			margin-top: 16px;

			& .tag_icon {
				height: 16px;
			}
		}
	}
</style>
