<script>
	import { module, loading, notify } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Marked from '$lib/marked.svelte';

	let comment = { ...$module.comment };
	let error = {};

	const submit = async () => {
		error = {};

		$loading = `Deleting comment . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/${comment.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		$loading = false;

		resp = await resp.json();

		if (resp.status == 200) {
			$module.update(resp.comments);
			$module = null;
			$notify.add('Comment Deleted');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle">Delete Comment</strong>

	<br />
	<br />

	<div class="comment">
		<Marked content={comment.comment} />
	</div>

	<br />

	<div class="error">Are you sure you want to delete this comment</div>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<br />

	<div class="line">
		<Button extra="hover_red" on:click={submit}>
			<Icon icon="delete" />
			Yes
		</Button>
		<Button
			on:click={() => {
				$module = null;
			}}
		>
			<Icon icon="close" />
			No
		</Button>
	</div>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.comment {
		padding: 1px var(--sp2);
		border-radius: var(--sp0);

		background-color: color-mix(in srgb, var(--cl1), transparent 80%);
		color: var(--ft1);
		font-size: 0.8rem;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
