<script>
	import { module } from '$lib/store.svelte.js';
	import { Form } from '$lib/layout';

	import Add from './file.add.svelte';
	import Mod from './file.mod.svelte';

	let item = $state(module.value.item);

	let ops = $state({
		key: item.key,
		files: item.files,
		title: item.title,

		count: item.content.split('@[file]').length - 1,
		active: item.files[0] || '/no_photo.png',
		error: {}
	});

	let add;
</script>

<Form title="Manage File" error={ops.error.error}>
	<Add bind:ops bind:this={add} />
	<Mod bind:ops onadd={() => add.add()} />
</Form>
