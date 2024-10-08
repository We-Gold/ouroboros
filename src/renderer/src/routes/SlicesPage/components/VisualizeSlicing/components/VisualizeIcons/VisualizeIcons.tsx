import { useContext } from 'react'
import styles from './VisualizeIcons.module.css'

import Camera from './assets/camera.svg?react'
import Information from './assets/information.svg?react'
import { AlertContext } from '@renderer/contexts/AlertContext'
import { WebGLRenderer } from 'three'

function VisualizeIcons({ gl }: { gl: WebGLRenderer | null }): JSX.Element {
	const { addAlert } = useContext(AlertContext)

	return (
		<div className={styles.visualizeIconsArea}>
			<VisualizeIcon
				icon={<Information />}
				onClick={() => {
					addAlert(
						'Use the mouse to interact with the rendering of the slices. For better visualization, only 1% of the slices are rendered.',
						'info'
					)
				}}
			/>
			<VisualizeIcon
				icon={<Camera />}
				onClick={() => {
					if (!gl) {
						addAlert('No rendering to save.', 'error')
						return
					}

					const link = document.createElement('a')
					link.setAttribute('download', 'ouroboros-slice-visualization.png')
					link.setAttribute(
						'href',
						gl.domElement
							.toDataURL('image/png')
							.replace('image/png', 'image/octet-stream')
					)
					link.click()
				}}
			/>
		</div>
	)
}

export default VisualizeIcons

function VisualizeIcon({ icon, onClick }: { icon: JSX.Element; onClick: () => void }): JSX.Element {
	return (
		<a className={styles.visualizeIcon} onClick={onClick}>
			{icon}
		</a>
	)
}
