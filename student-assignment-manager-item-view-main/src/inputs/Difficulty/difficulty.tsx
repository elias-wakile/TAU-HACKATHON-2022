import { Flex, FlexProps } from '@chakra-ui/react'
import { useState } from 'react'
import { theme } from '../../theme'
import { DifficultyBox } from './difficulty-box'

interface IDifficultyProps extends FlexProps {
	value: number
	onChangeHandler: (index: number) => void
}

const baseURL = 'https://student-assignment-manager-test-bucket.s3.amazonaws.com/'

export const Difficulty = ({ value, onChangeHandler, ...props }: IDifficultyProps) => {
	const [isHover, setIsHover] = useState(false)
	const [hoveredIndex, setHoveredIndex] = useState(0)
	return (
		<Flex {...props} data-id='Difficulty'>
			{theme.diffcultyColors.map((c, i) => {
				return (
					<DifficultyBox
						data-id={`difficulty-box-${i}`}
						key={`difficulty-box-${i}`}
						onHover={() => {
							setIsHover(true)
							setHoveredIndex(i)
						}}
						onUnHover={() => setIsHover(false)}
						src={
							isHover
								? i > hoveredIndex
									? `${baseURL}${0}.png`
									: `${baseURL}${i + 1}.png`
								: i > value
								? `${baseURL}${0}.png`
								: `${baseURL}${i + 1}.png`
						}
						onClick={() => onChangeHandler(i)}
					/>
				)
			})}
		</Flex>
	)
}
