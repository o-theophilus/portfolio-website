<script>
	import Content from '$lib/content.svelte';
	import Group from './skill.group.svelte';
	import Observe from '$lib/observe.svelte';

	let skills = [
		{ name: 'HTML', value: 95 },
		{ name: 'CSS', value: 90 },
		{ name: 'JavaScript', value: 65 },
		{ name: 'React', value: 50 },
		{ name: 'Svelte', value: 87 },
		{ name: 'Python', value: 90 },
		{ name: 'Flask', value: 85 },
		{ name: 'Postgres', value: 65 },
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

<Content fit>
	<div class="comp">
		<Observe let:intersecting>
			<div class="observe" class:intersecting>
				<strong class="ititle dark"> My Skills </strong>
				<br />
				I am a multidisciplinary designer with a passion for creating impactful designs for web and print.
				From logos to brochures, websites to social media graphics, I've got you covered.
			</div>
		</Observe>

		<div class="group">
			<Group list={skills} name="Programming Skills" icon="code" />
			<Group list={tools} name="Software Skills" icon="wysiwyg" />
		</div>
	</div>
</Content>

<style>
	.comp {
		margin: var(--sp4) 0;
	}
	
	.group {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);
		margin: var(--sp2) 0;
	}

	@media screen and (min-width: 500px) {
		.group {
			flex-direction: unset;
		}
	}
</style>
