<script>
	import { module } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	import Form from './share_form.svelte';

	let { item } = $props();
</script>

<Button onclick={() => module.open(Form, item)}>
	<Icon icon="share-2" />
	Share
</Button>
