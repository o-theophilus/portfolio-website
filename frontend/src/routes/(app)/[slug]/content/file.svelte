<script>
	import { Form } from '$lib/layout';
	import { module } from '$lib/store.svelte.js';

	import Add from './file.add.svelte';
	import Mod from './file.mod.svelte';

	let post = $state(module.value.post);

	let ops = $state({
		key: post.key,
		files: post.files,
		title: post.title,

		count: post.content.split('@[file]').length - 1,
		active: post.files[0] || '/no_photo.png',
		error: {}
	});

	let add;
</script>

<Form title="Manage File" error={ops.error.error}>
	<Add bind:ops bind:this={add} />
	<Mod bind:ops onadd={() => add.add()} />
</Form>
