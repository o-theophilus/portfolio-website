<script>
	import Observe from '$lib/observe.svelte';
	import Content from '$lib/content.svelte';
	import Skill from './page.5_about.skill_item.svelte';

	let skills = [
		{ name: 'HTML', value: 95 },
		{ name: 'CSS', value: 90 },
		{ name: 'JavaScript', value: 65 },
		{ name: 'React', value: 50 },
		{ name: 'Svelte / SvelteKit', value: 87 },
		{ name: 'Python', value: 90 },
		{ name: 'Flask', value: 85 }
	];

	let tools = [
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

<Content>
	<br /> <br />
	<strong class="big">Programming Skills / Stack</strong>
	<br /><br />
	{#each skills as ent}
		<div class="skill">
			<div class="name">
				{ent.name}
			</div>
			<div class="chat">
				<Skill num={ent.value} />
			</div>
		</div>
	{/each}
	<br /><br />

	<strong class="big">Software Skills</strong>
	<br /> <br />
	{#each tools as ent}
		<div class="skill">
			<div class="name">
				{ent.name}
			</div>
			<div class="chat">
				<Skill num={ent.value} />
			</div>
		</div>
	{/each}
	<br /> <br />
</Content>

<style>
	strong {
		color: var(--accent1);
	}
	.skill {
		display: flex;
		gap: 20px;
		align-items: center;
	}
	.name {
		width: 150px;
		flex-shrink: 0;
	}
	.chat {
		width: 100%;
	}
</style>
