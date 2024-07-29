<script>
	import Content from '$lib/content.svelte';
	import Icon from '$lib/icon.svelte';
	import One from './skill.one.svelte';

	let skills = [
		{ name: 'HTML', value: 95 },
		{ name: 'CSS', value: 90 },
		{ name: 'JavaScript', value: 65 },
		{ name: 'React', value: 50 },
		{ name: 'Svelte', value: 87 },
		{ name: 'Python', value: 90 },
		{ name: 'Flask', value: 85 }
	];

	let tools = [
		{ name: 'Figma', value: 80 },
		{ name: 'CorelDRAW', value: 94 },
		{ name: 'Photoshop', value: 79 },
		// { name: 'Premiere Pro', value: 53 },
		{ name: 'Blender 3D', value: 80 },
		{ name: 'Verge3D', value: 80 },
		{ name: 'SketchUp', value: 85 },
		{ name: 'Godot', value: 30 }
	];
</script>

<Content fit>
	<div class="comp">
		<div class="group">
			<div class="line">
				<div class="icon">
					<Icon icon="code" size="1.5" />
				</div>
				<div class="title">Programming Skills</div>
			</div>

			{#each skills as x}
				<One one={x} />
			{/each}
		</div>

		<div class="group">
			<div class="line">
				<div class="icon">
					<Icon icon="wysiwyg" size="1.5" />
				</div>
				<div class="title">Software Skills</div>
			</div>

			{#each tools as x}
				<One one={x} />
			{/each}
		</div>
	</div>
</Content>

<style>
	.comp {
		display: flex;
		flex-direction: column;
		gap: var(--sp3);

		margin: var(--sp2) 0;
	}

	@media screen and (min-width: 500px) {
		.comp {
			flex-direction: unset;
			gap: var(--sp4);
		}
	}

	.group {
		width: 100%;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		color: var(--ft1);
		fill: currentColor;
	}

	.icon {
		--size: 60px;

		display: flex;
		justify-content: center;
		align-items: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		background-color: var(--bg2);
		border-radius: var(--sp0);
	}

	.title {
		font-weight: 800;
		font-size: 1.1rem;
	}
</style>
