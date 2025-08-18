<script>
	import { module } from '$lib/store.svelte.js';
	import { Form } from '$lib/layout';

	import Add from './file.add.svelte';
	import Mod from './file.mod.svelte';

	let post = $state(module.value.post);

	let ops = $state({
		key: post.key,
		files: post.files,
		title: post.title,

		count: post.content.split('@[file]').length - 1,
		active: post.files[0] || null,
		error: {}
	});

	let add;
</script>

<Form title="Manage File" error={ops.error.error}>
	<Add bind:this={add} bind:ops />
	<Mod bind:ops onadd={() => add.add()} />
</Form>
