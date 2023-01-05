<script>
	import { is_admin } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';
	import Content from '$lib/comp/content.svelte';
	import Meta from '$lib/comp/meta.svelte';
</script>

<Meta title="Admin Dashboard | Theophilus" description="Admin Dashboard" />

<Content>
	<Button
		on:click={() => {
			$is_admin = !$is_admin;
		}}
	>
		GET {$is_admin ? 'OUT' : 'IN'}
	</Button>
</Content>
