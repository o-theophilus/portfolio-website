<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { module } from '$lib/store.svelte.js';

	import Form from './share_form.svelte';

	let { post } = $props();
</script>

<Button onclick={() => module.open(Form, post)}>
	<Icon icon="share-2" />
	Share
</Button>
